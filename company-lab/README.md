# Company Lab

Production-like two-server internal IT operations portal.

## Architecture

- `srv-01` runs the backend API.
- `srv-02` serves the frontend through nginx.
- nginx on `srv-02` proxies `/api/` requests to `srv-01:3000`.
- Backend runs as a systemd service.
- SQLite is used as the local application database.

## Components

| Component | Host | Role |
|---|---|---|
| Backend API | srv-01 | FastAPI application |
| Frontend | srv-02 | Static HTML/CSS/JS |
| Reverse proxy | srv-02 | nginx |
| Database | srv-01 | SQLite |
| Process manager | srv-01 | systemd |

## API endpoints

| Endpoint | Purpose |
|---|---|
| `/api/health` | Backend healthcheck |
| `/api/status` | Backend status |
| `/api/summary` | Dashboard summary |
| `/api/tickets` | Ticket list and ticket creation |
| `/api/assets` | Asset inventory |
| `/api/servers` | Server inventory |
| `/api/services` | Service health inventory |
| `/api/changes` | Change log |
| `/api/audit` | Recent audit events |
| `/docs` | FastAPI Swagger documentation |

## Operational tests

Run on `srv-02`:

```bash
curl -I http://localhost
curl -s http://localhost/nginx-health
curl -s http://localhost/api/health
curl -s http://localhost/api/summary
curl -I http://localhost/docs

Expected result:

nginx returns 200 OK
/nginx-health returns nginx ok
/api/health returns backend status
/api/summary returns dashboard counters
/docs returns FastAPI documentation
Deployment notes

Backend files live on srv-01:

/opt/company-backend/

Backend data lives on srv-01:

/var/lib/company-backend/company.db

Frontend files live on srv-02:

/var/www/company-frontend/

nginx config lives on srv-02:

/etc/nginx/sites-available/company-lab
Skills practiced
Linux service management
systemd
FastAPI
SQLite
nginx reverse proxy
static frontend deployment
API testing with curl
basic operational documentation
