# Company Lab

Small internal company-style lab built on two VMs.

The goal of this lab is to understand how a basic web application is split into frontend, backend, API, reverse proxy and database layers.

## Machines

| Machine | OS | IP | Role |
|---|---|---|---|
| `srv-01` | Ubuntu | `192.168.122.10` | backend API + SQLite |
| `srv-02` | Debian | `192.168.122.50` | nginx + frontend + reverse proxy |
| `archlinux` | Arch Linux | `192.168.1.92` | host / hypervisor |

## Current flow

```text
Browser / host
  ↓
srv-02 nginx
  ↓
frontend files
  ↓
/api requests
  ↓
nginx reverse proxy
  ↓
srv-01 backend
  ↓
SQLite database
What was built
srv-01 backend
created dedicated system user: company-backend
created backend directories:
/opt/company-backend
/etc/company-backend
/var/lib/company-backend
created SQLite database:
/var/lib/company-backend/company.db
created Python backend API:
/opt/company-backend/app.py
created systemd service:
company-backend.service
enabled backend autostart
srv-02 frontend
configured nginx to serve frontend from:
/var/www/company-frontend
created frontend files:
index.html
style.css
app.js
configured nginx reverse proxy:
/api/ → http://192.168.122.10:3000
Working URLs

Frontend:

http://192.168.122.50

Backend through nginx:

http://192.168.122.50/api/status

Backend direct:

http://192.168.122.10:3000/api/status
Quick checks

On srv-01:

systemctl status company-backend --no-pager
curl http://127.0.0.1:3000/api/status

On srv-02:

systemctl status nginx --no-pager
nginx -t
curl http://127.0.0.1/api/status

From the host:

curl http://192.168.122.50
curl http://192.168.122.50/api/status
Notes

This is a learning lab, not a production deployment.

Current limitations:

test data only
SQLite used for simplicity
login endpoint is lab-only
no TLS inside the VM network
no monitoring yet
no backup procedure yet
