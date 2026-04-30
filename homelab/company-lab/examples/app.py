import json
import os
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer


APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", "3000"))
DB_PATH = os.environ.get("DB_PATH", "/var/lib/company-backend/company.db")


def query_all(sql, params=()):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def query_one(sql, params=()):
    rows = query_all(sql, params)
    return rows[0] if rows else None


class Handler(BaseHTTPRequestHandler):
    def send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")

        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length)

        if not raw_body:
            return {}

        return json.loads(raw_body.decode("utf-8"))

    def do_GET(self):
        if self.path == "/api/status":
            self.send_json(200, {
                "service": "company-backend",
                "host": "srv-01",
                "status": "ok",
                "database": DB_PATH
            })

        elif self.path == "/api/employees":
            employees = query_all("""
                SELECT id, full_name, department, position, email
                FROM employees
                ORDER BY id
            """)
            self.send_json(200, employees)

        elif self.path == "/api/tickets":
            tickets = query_all("""
                SELECT id, title, status, priority, assigned_to
                FROM tickets
                ORDER BY id
            """)
            self.send_json(200, tickets)

        elif self.path == "/api/assets":
            assets = query_all("""
                SELECT id, asset_type, name, owner, status
                FROM assets
                ORDER BY id
            """)
            self.send_json(200, assets)

        elif self.path == "/api/servers":
            servers = query_all("""
                SELECT id, hostname, ip_address, role, os, status
                FROM servers
                ORDER BY id
            """)
            self.send_json(200, servers)

        elif self.path == "/api/summary":
            employees_count = query_one("SELECT COUNT(*) AS count FROM employees")["count"]
            open_tickets_count = query_one("SELECT COUNT(*) AS count FROM tickets WHERE status != 'closed'")["count"]
            assets_count = query_one("SELECT COUNT(*) AS count FROM assets")["count"]
            servers_count = query_one("SELECT COUNT(*) AS count FROM servers")["count"]

            self.send_json(200, {
                "employees": employees_count,
                "open_tickets": open_tickets_count,
                "assets": assets_count,
                "servers": servers_count
            })

        else:
            self.send_json(404, {
                "error": "not found",
                "path": self.path
            })

    def do_POST(self):
        if self.path == "/api/login":
            try:
                data = self.read_json_body()
            except Exception:
                self.send_json(400, {
                    "success": False,
                    "message": "Invalid JSON"
                })
                return

            username = data.get("username")
            password = data.get("password")

            user = query_one("""
                SELECT username, role
                FROM users
                WHERE username = ? AND password = ?
            """, (username, password))

            if user:
                self.send_json(200, {
                    "success": True,
                    "message": "Login successful",
                    "user": user
                })
            else:
                self.send_json(401, {
                    "success": False,
                    "message": "Invalid username or password"
                })

        else:
            self.send_json(404, {
                "error": "not found",
                "path": self.path
            })


if __name__ == "__main__":
    print(f"Starting company-backend on {APP_HOST}:{APP_PORT}")
    print(f"Using database: {DB_PATH}")
    HTTPServer((APP_HOST, APP_PORT), Handler).serve_forever()
