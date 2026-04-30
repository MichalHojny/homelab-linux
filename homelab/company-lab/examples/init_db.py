import os
import sqlite3

DB_PATH = os.environ.get("DB_PATH", "/var/lib/company-backend/company.db")

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS assets;
DROP TABLE IF EXISTS servers;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    department TEXT NOT NULL,
    position TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    priority TEXT NOT NULL,
    assigned_to TEXT NOT NULL
);

CREATE TABLE assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_type TEXT NOT NULL,
    name TEXT NOT NULL,
    owner TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE servers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostname TEXT NOT NULL,
    ip_address TEXT NOT NULL,
    role TEXT NOT NULL,
    os TEXT NOT NULL,
    status TEXT NOT NULL
);
""")

cursor.executemany(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    [
        ("admin", "admin123", "admin"),
        ("marek", "test123", "employee"),
        ("anna", "test123", "employee"),
    ],
)

cursor.executemany(
    "INSERT INTO employees (full_name, department, position, email) VALUES (?, ?, ?, ?)",
    [
        ("Adam Nowak", "IT", "Linux Administrator", "adam.nowak@company.local"),
        ("Anna Kowalska", "HR", "HR Specialist", "anna.kowalska@company.local"),
        ("Marek Zielinski", "Support", "Helpdesk Technician", "marek.zielinski@company.local"),
        ("Jan Wisniewski", "Security", "SOC Analyst L1", "jan.wisniewski@company.local"),
        ("Ewa Kaminska", "Operations", "NOC Operator", "ewa.kaminska@company.local"),
    ],
)

cursor.executemany(
    "INSERT INTO tickets (title, status, priority, assigned_to) VALUES (?, ?, ?, ?)",
    [
        ("Laptop nie uruchamia sie", "open", "high", "Marek Zielinski"),
        ("Problem z VPN", "in_progress", "medium", "Adam Nowak"),
        ("Monitor do wymiany", "closed", "low", "Marek Zielinski"),
        ("Alert: wysoki load na srv-01", "open", "high", "Ewa Kaminska"),
        ("Nowe konto dla pracownika", "in_progress", "medium", "Anna Kowalska"),
    ],
)

cursor.executemany(
    "INSERT INTO assets (asset_type, name, owner, status) VALUES (?, ?, ?, ?)",
    [
        ("Laptop", "Dell Latitude 5420", "Adam Nowak", "assigned"),
        ("Laptop", "Lenovo ThinkPad T14", "Anna Kowalska", "assigned"),
        ("Monitor", "LG 27 inch", "Marek Zielinski", "assigned"),
        ("Phone", "Samsung A54", "Ewa Kaminska", "assigned"),
        ("Router", "MikroTik lab-router", "IT Storage", "spare"),
    ],
)

cursor.executemany(
    "INSERT INTO servers (hostname, ip_address, role, os, status) VALUES (?, ?, ?, ?, ?)",
    [
        ("srv-01", "192.168.122.10", "backend/api/database", "Ubuntu", "online"),
        ("srv-02", "192.168.122.50", "frontend/nginx", "Debian", "online"),
        ("archlinux", "192.168.1.92", "hypervisor/host", "Arch Linux", "online"),
    ],
)

connection.commit()
connection.close()

print(f"Database initialized: {DB_PATH}")
