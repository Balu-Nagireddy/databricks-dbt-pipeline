# Deployment Guide — Prism Analytics Analytics Platform

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Environment Configuration](#2-environment-configuration)
3. [Local Development Deployment](#3-local-development-deployment)
4. [Docker Compose Production Deployment](#4-docker-compose-production-deployment)
5. [Manual Bare-Metal Deployment](#5-manual-bare-metal-deployment)
6. [Running the Spark Pipeline](#6-running-the-spark-pipeline)
7. [Required GitHub Secrets](#7-required-github-secrets)
8. [Rollback Procedure](#8-rollback-procedure)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Prerequisites

| Tool | Minimum Version | Purpose |
|---|---|---|
| Python | 3.12 | Backend + pipeline |
| Node.js | 20 LTS | Frontend build |
| Docker Desktop | 24+ | Containerized deployment |
| Java (JDK) | 11 or 17 | PySpark |
| PostgreSQL client | 15 | Warehouse validation (optional) |

---

## 2. Environment Configuration

Copy `.env.example` to `.env` and fill in all values:

```bash
cp .env.example .env
```

### Required Variables

```env
# Application
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO

# Supabase PostgreSQL
SUPABASE_DB_HOST=aws-1-ap-south-1.pooler.supabase.com
SUPABASE_DB_PORT=6543
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.<project-ref>
SUPABASE_DB_PASSWORD=<your-password>
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/postgres

# FastAPI
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
```

> [!CAUTION]
> Never commit `.env` to Git. The `.gitignore` already excludes it. Use `.env.example` for documentation only.

---

## 3. Local Development Deployment

```bash
# Python environment
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows
pip install -r requirements.txt

# Start FastAPI backend (port 8000)
python -m src.backend.app

# Start React frontend in new terminal (port 5173)
cd src/frontend
npm install
npm run dev
```

Access points:
- Dashboard: http://localhost:5173/
- API Swagger: http://localhost:8000/api/v1/docs
- API ReDoc: http://localhost:8000/api/v1/redoc

---

## 4. Docker Compose Production Deployment

### First Deployment

```bash
# 1. Configure environment
cp .env.example .env
nano .env          # Fill in all values

# 2. Build and start all services
docker compose up -d --build

# 3. Verify health
docker compose ps
docker compose logs backend --tail=20
docker compose logs frontend --tail=20
```

### Expected Output

```
NAME                  STATUS
prism-backend      Up (healthy)
prism-frontend     Up (healthy)
```

Access points:
- Dashboard: http://localhost:80/
- API: http://localhost:8000/api/v1/docs
- Metrics: http://localhost:8000/metrics

### Service Management

```bash
# Stop all services
docker compose down

# Restart a single service
docker compose restart backend

# View logs (follow)
docker compose logs -f backend

# Rebuild after code changes
docker compose up -d --build backend
```

---

## 5. Manual Bare-Metal Deployment

For servers without Docker:

```bash
# 1. Install Python deps in a virtualenv
python3.12 -m venv /opt/prism/venv
/opt/prism/venv/bin/pip install -r requirements.txt

# 2. Copy application source
cp -r src/ /opt/prism/src/

# 3. Start Uvicorn via systemd (see scripts/prism-backend.service)
sudo systemctl enable prism-backend
sudo systemctl start prism-backend

# 4. Build React and deploy to nginx
cd src/frontend
npm ci && npm run build
sudo cp -r dist/* /var/www/prism/
sudo systemctl reload nginx
```

---

## 6. Running the Spark Pipeline

Run in order:

```bash
# Activate venv first
source .venv/bin/activate

# Phase 2: Bronze (raw CSV → Parquet)
python -m src.pipeline.bronze

# Phase 3: Silver (clean + validate)
python -m src.pipeline.silver

# Phase 4: Gold (business marts)
python -m src.pipeline.gold

# Phase 6: Warehouse load
python -m src.warehouse.loader

# Phase 7: dbt semantic layer
cd analytics
dbt deps --profiles-dir ~/.dbt
dbt run --profiles-dir ~/.dbt
dbt test --profiles-dir ~/.dbt
```

---

## 7. Required GitHub Secrets

Configure these in **Settings → Secrets and variables → Actions**:

| Secret Name | Description |
|---|---|
| `DATABASE_URL` | Full SQLAlchemy connection string |
| `SUPABASE_DB_HOST` | Supabase pooler host |
| `SUPABASE_DB_PORT` | Usually `6543` |
| `SUPABASE_DB_NAME` | `postgres` |
| `SUPABASE_DB_USER` | `postgres.<project-ref>` |
| `SUPABASE_DB_PASSWORD` | Supabase DB password |

---

## 8. Rollback Procedure

```bash
# Rollback to previous Docker image
docker compose down
git checkout HEAD~1
docker compose up -d --build

# Or rollback a specific service
docker stop prism-backend
docker run -d --name prism-backend prism-backend:<previous-tag>
```

---

## 9. Troubleshooting

| Symptom | Diagnosis | Fix |
|---|---|---|
| Backend unhealthy | DB unreachable | Check `DATABASE_URL` in `.env` |
| Frontend 502 | Backend not running | `docker compose restart backend` |
| dbt parse fails | profiles.yml missing | Create `~/.dbt/profiles.yml` |
| Spark OOM | Java heap too small | Set `JAVA_OPTS=-Xmx4g` |
| `psycopg2` import error | Binary not installed | `pip install psycopg2-binary` |
| Port 80 in use | Another service on 80 | Change `ports: "8080:80"` in compose |
