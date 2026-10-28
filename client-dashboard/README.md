# Client Dashboard

Internal tool: clients → projects → tasks, with an overdue/blocked dashboard.
FastAPI + SQLite, single shared password. Served over HTTPS by Caddy.

## Run locally
```bash
pip install -r requirements-dev.txt
APP_PASSWORD=pw SECRET_KEY=dev COOKIE_SECURE=0 uvicorn app.main:app --reload
pytest
```

## Deploy to a DigitalOcean droplet
1. Create an Ubuntu droplet; point an A record (e.g. `dashboard.yourdomain.com`) at its IP.
2. `ssh root@IP`, then `mkdir -p /opt/client-dashboard` and create `/opt/client-dashboard/.env` from `.env.example`.
3. From this folder: `./deploy.sh root@IP`
4. Open `https://<DOMAIN>` — Caddy provisions the TLS cert automatically (ports 80/443 must be open).

Update: re-run `./deploy.sh`. Data persists in the `appdata` Docker volume.
Backup: `docker compose cp app:/data/app.db ./backup.db`

## Notes
- Shared-password auth: fine for a small trusted team; add per-user accounts if you need audit trails.
- For extra safety, restrict ports 80/443 to your office/VPN IPs with a DO Cloud Firewall.
