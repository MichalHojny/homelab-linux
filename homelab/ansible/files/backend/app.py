import os
import platform
import socket
import sqlite3
import time
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


APP_NAME = "company-backend"
APP_VERSION = "2.0.0"
ENVIRONMENT = "homelab"
START_TIME = time.time()

DB_PATH = os.environ.get("DB_PATH", "/var/lib/company-backend/company.db")

app = FastAPI(
    title="ZrytyBeret IT Operations API",
    description="Internal IT operations portal API for homelab company-lab project.",
    version=APP_VERSION,
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def query_all(sql: str, params: tuple = ()):
    connection = connect_db()
    try:
        rows = connection.execute(sql, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def query_one(sql: str, params: tuple = ()):
    rows = query_all(sql, params)
    return rows[0] if rows else None


def execute(sql: str, params: tuple = ()):
    connection = connect_db()
    try:
        cursor = connection.execute(sql, params)
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def table_columns(table_name: str):
    rows = query_all(f"PRAGMA table_info({table_name})")
    return {row["name"] for row in rows}


def add_column_if_missing(table: str, column: str, definition: str):
    columns = table_columns(table)
    if column not in columns:
        execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def audit(event_type: str, message: str, entity_type: Optional[str] = None, entity_id: Optional[int] = None):
    execute(
        """
        INSERT INTO audit_log (created_at, event_type, entity_type, entity_id, message)
        VALUES (?, ?, ?, ?, ?)
        """,
        (now_iso(), event_type, entity_type, entity_id, message),
    )


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            email TEXT NOT NULL
        )
        """
    )

    execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            priority TEXT NOT NULL DEFAULT 'medium',
            assigned_to TEXT,
            description TEXT,
            created_at TEXT,
            updated_at TEXT
        )
        """
    )

    execute(
        """
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_type TEXT NOT NULL,
            name TEXT NOT NULL,
            owner TEXT,
            status TEXT NOT NULL DEFAULT 'active'
        )
        """
    )

    execute(
        """
        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hostname TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            role TEXT NOT NULL,
            os TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'online'
        )
        """
    )

    execute(
        """
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            host TEXT NOT NULL,
            port TEXT,
            status TEXT NOT NULL DEFAULT 'unknown',
            description TEXT,
            last_check TEXT
        )
        """
    )

    execute(
        """
        CREATE TABLE IF NOT EXISTS changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            service TEXT,
            risk TEXT NOT NULL DEFAULT 'medium',
            status TEXT NOT NULL DEFAULT 'planned',
            description TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    execute(
        """
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            event_type TEXT NOT NULL,
            entity_type TEXT,
            entity_id INTEGER,
            message TEXT NOT NULL
        )
        """
    )

    # Safe migrations for older database schema.
    add_column_if_missing("tickets", "description", "TEXT")
    add_column_if_missing("tickets", "created_at", "TEXT")
    add_column_if_missing("tickets", "updated_at", "TEXT")

    add_column_if_missing("assets", "location", "TEXT")
    add_column_if_missing("assets", "notes", "TEXT")

    add_column_if_missing("servers", "environment", "TEXT")
    add_column_if_missing("servers", "notes", "TEXT")
    add_column_if_missing("servers", "last_seen", "TEXT")

    seed_initial_data()
    audit("backend_started", f"{APP_NAME} {APP_VERSION} started", "service", None)


def seed_initial_data():
    if query_one("SELECT COUNT(*) AS count FROM services")["count"] == 0:
        services = [
            ("company-backend", "srv-01", "3000", "online", "FastAPI backend API", now_iso()),
            ("nginx-frontend", "srv-02", "80", "online", "nginx static frontend and reverse proxy", now_iso()),
            ("libvirt-dns", "archlinux", "53", "online", "dnsmasq DNS for libvirt VM network", now_iso()),
            ("guacamole", "archlinux", "docker", "planned", "Browser-based remote access", now_iso()),
            ("cloudflared", "archlinux", "tunnel", "planned", "Cloudflare Tunnel external access", now_iso()),
        ]

        for item in services:
            execute(

                """
                INSERT INTO services (name, host, port, status, description, last_check)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                item,
            )

    if query_one("SELECT COUNT(*) AS count FROM changes")["count"] == 0:
        changes = [
            (
                "Deploy FastAPI backend v2",
                "company-backend",
                "medium",
                "in_progress",
                "Upgrade simple Python HTTP backend to FastAPI with API documentation.",
                now_iso(),
            ),
            (
                "Add nginx API reverse proxy",
                "nginx",
                "medium",
                "planned",
                "Route /api traffic from srv-02 nginx to srv-01 backend.",
                now_iso(),
            ),
            (
                "Document company-lab architecture",
                "company-lab",
                "low",
                "planned",
                "Add architecture, troubleshooting and deployment documentation.",
                now_iso(),
            ),
        ]

        for item in changes:
            execute(
                """
                INSERT INTO changes (title, service, risk, status, description, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                item,
            )


class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    priority: str = "medium"
    assigned_to: Optional[str] = None
    description: Optional[str] = None


class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    description: Optional[str] = None


class ChangeCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    service: Optional[str] = None
    risk: str = "medium"
    status: str = "planned"
    description: Optional[str] = None


def validate_status(status: str):
    allowed = {"open", "in_progress", "waiting", "resolved", "closed"}
    if status not in allowed:
        raise HTTPException(status_code=400, detail=f"Invalid status. Allowed: {sorted(allowed)}")


def validate_priority(priority: str):
    allowed = {"low", "medium", "high", "critical"}
    if priority not in allowed:
        raise HTTPException(status_code=400, detail=f"Invalid priority. Allowed: {sorted(allowed)}")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": APP_NAME,
        "version": APP_VERSION,
        "host": socket.gethostname(),
        "timestamp": now_iso(),
    }


@app.get("/api/status")
def status():
    return {
        "status": "ok",
        "service": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "host": socket.gethostname(),
        "database": DB_PATH,
        "uptime_seconds": int(time.time() - START_TIME),
        "timestamp": now_iso(),
    }


@app.get("/api/system")
def system_info():
    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "uptime_seconds": int(time.time() - START_TIME),
        "timestamp": now_iso(),
    }


@app.get("/api/summary")
def summary():
    employees_count = query_one("SELECT COUNT(*) AS count FROM employees")["count"]
    open_tickets_count = query_one("SELECT COUNT(*) AS count FROM tickets WHERE status != 'closed'")["count"]
    critical_tickets_count = query_one("SELECT COUNT(*) AS count FROM tickets WHERE priority = 'critical'")["count"]
    assets_count = query_one("SELECT COUNT(*) AS count FROM assets")["count"]
    servers_count = query_one("SELECT COUNT(*) AS count FROM servers")["count"]
    online_servers_count = query_one("SELECT COUNT(*) AS count FROM servers WHERE status = 'online'")["count"]
    services_count = query_one("SELECT COUNT(*) AS count FROM services")["count"]
    open_changes_count = query_one("SELECT COUNT(*) AS count FROM changes WHERE status != 'done'")["count"]

    return {
        "employees": employees_count,
        "open_tickets": open_tickets_count,
        "critical_tickets": critical_tickets_count,
        "assets": assets_count,
        "servers": servers_count,
        "online_servers": online_servers_count,
        "services": services_count,
        "open_changes": open_changes_count,
        "timestamp": now_iso(),
    }


@app.get("/api/employees")
def employees():
    return query_all(
        """
        SELECT id, full_name, department, position, email
        FROM employees
        ORDER BY id
        """
    )


@app.get("/api/tickets")
def tickets():
    return query_all(
        """
        SELECT id, title, status, priority, assigned_to, description, created_at, updated_at
        FROM tickets
        ORDER BY
            CASE priority
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                WHEN 'low' THEN 4
                ELSE 5
            END,
            id DESC
        """
    )


@app.post("/api/tickets", status_code=201)
def create_ticket(ticket: TicketCreate):
    validate_priority(ticket.priority)

    created_at = now_iso()
    ticket_id = execute(
        """
        INSERT INTO tickets (title, status, priority, assigned_to, description, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ticket.title,
            "open",
            ticket.priority,
            ticket.assigned_to,
            ticket.description,
            created_at,
            created_at,
        ),
    )

    audit("ticket_created", f"Ticket created: {ticket.title}", "ticket", ticket_id)

    return query_one(
        """
        SELECT id, title, status, priority, assigned_to, description, created_at, updated_at
        FROM tickets
        WHERE id = ?
        """,
        (ticket_id,),
    )


@app.patch("/api/tickets/{ticket_id}")
def update_ticket(ticket_id: int, update: TicketUpdate):
    existing = query_one("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Ticket not found")

    new_status = update.status if update.status is not None else existing["status"]
    new_priority = update.priority if update.priority is not None else existing["priority"]
    new_assigned_to = update.assigned_to if update.assigned_to is not None else existing["assigned_to"]
    new_description = update.description if update.description is not None else existing["description"]

    validate_status(new_status)
    validate_priority(new_priority)

    execute(
        """
        UPDATE tickets
        SET status = ?, priority = ?, assigned_to = ?, description = ?, updated_at = ?
        WHERE id = ?
        """,
        (new_status, new_priority, new_assigned_to, new_description, now_iso(), ticket_id),
    )

    audit(
        "ticket_updated",
        f"Ticket {ticket_id} updated: status={new_status}, priority={new_priority}",
        "ticket",
        ticket_id,
    )

    return query_one(
        """
        SELECT id, title, status, priority, assigned_to, description, created_at, updated_at
        FROM tickets
        WHERE id = ?
        """,
        (ticket_id,),
    )


@app.get("/api/assets")
def assets():
    return query_all(
        """
        SELECT id, asset_type, name, owner, status
        FROM assets
        ORDER BY id
        """
    )


@app.get("/api/servers")
def servers():
    return query_all(
        """
        SELECT id, hostname, ip_address, role, os, status
        FROM servers
        ORDER BY id
        """
    )


@app.get("/api/services")
def services():
    return query_all(
        """
        SELECT id, name, host, port, status, description, last_check
        FROM services
        ORDER BY id
        """
    )


@app.get("/api/changes")
def changes():
    return query_all(
        """
        SELECT id, title, service, risk, status, description, created_at
        FROM changes
        ORDER BY id DESC
        """
    )


@app.post("/api/changes", status_code=201)
def create_change(change: ChangeCreate):
    change_id = execute(
        """
        INSERT INTO changes (title, service, risk, status, description, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (change.title, change.service, change.risk, change.status, change.description, now_iso()),
    )

    audit("change_created", f"Change created: {change.title}", "change", change_id)

    return query_one(
        """
        SELECT id, title, service, risk, status, description, created_at
        FROM changes
        WHERE id = ?
        """,
        (change_id,),
    )


@app.get("/api/audit")
def audit_log():
    return query_all(
        """
        SELECT id, created_at, event_type, entity_type, entity_id, message
        FROM audit_log
        ORDER BY id DESC
        LIMIT 50
        """
    )
