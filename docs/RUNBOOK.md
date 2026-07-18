# Operational Runbook — Prism Analytics Analytics Platform

This runbook covers the most common operational tasks performed by engineers managing the platform in production.

---

## 1. Daily Health Check

```bash
# Verify all containers are healthy
docker compose ps

# Check API health endpoint
curl http://localhost:8000/api/v1/health

# Expected response:
# {"status":"ok","database":"connected","version":"1.0.0","timestamp":"..."}

# Check Prometheus metrics endpoint
curl -s http://localhost:8000/metrics | grep http_requests_total
```

---

## 2. Restart Services

```bash
# Restart backend only
docker compose restart backend

# Restart frontend only
docker compose restart frontend

# Full restart
docker compose down && docker compose up -d
```

---

## 3. View Logs

```bash
# Live backend logs (Ctrl+C to stop)
docker compose logs -f backend

# Last 100 lines of backend logs
docker compose logs --tail=100 backend

# Frontend nginx access logs
docker compose logs --tail=50 frontend

# Filter for errors only
docker compose logs backend 2>&1 | grep ERROR
```

---

## 4. Run the Full Pipeline

Run the complete data pipeline from raw CSV to warehouse:

```bash
# Activate virtualenv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# Step 1: Bronze
python -m src.pipeline.bronze
# Expected: "Bronze layer completed successfully"

# Step 2: Silver
python -m src.pipeline.silver
# Expected: "Silver layer completed successfully"

# Step 3: Gold
python -m src.pipeline.gold
# Expected: "Gold layer completed successfully"

# Step 4: Load warehouse
python -m src.warehouse.loader
# Expected: All tables loaded

# Step 5: dbt refresh
cd analytics
dbt run --profiles-dir ~/.dbt
dbt test --profiles-dir ~/.dbt
```

---

## 5. Run Tests

```bash
# Backend integration tests
pytest tests/backend/ -v --tb=short

# Frontend unit tests
cd src/frontend && npm test

# dbt tests
cd analytics && dbt test --profiles-dir ~/.dbt
```

---

## 6. Re-Initialize the Warehouse Schema

If tables need to be recreated from scratch:

```bash
# Apply schema DDL to Supabase
psql "$DATABASE_URL" -f docs/schema_init.sql
```

---

## 7. Rebuild Docker Images After Code Changes

```bash
# Rebuild backend only
docker compose up -d --build backend

# Rebuild frontend only
docker compose up -d --build frontend

# Rebuild everything
docker compose up -d --build
```

---

## 8. Check Database Connectivity

```bash
# Python connectivity test
python -c "
from src.backend.database import ping_db
print('DB OK' if ping_db() else 'DB FAILED')
"

# Direct psql connection
psql "$DATABASE_URL" -c "SELECT current_timestamp, current_database();"
```

---

## 9. Clear Prometheus Metrics (Dev Only)

```bash
# Restart backend to reset in-memory metrics
docker compose restart backend
```

---

## 10. Emergency: Take API Offline

```bash
# Stops API but keeps frontend up (shows error state)
docker compose stop backend

# Bring back online
docker compose start backend
```

---

## 11. Common Error Resolution

### "connection refused" on API health check
```bash
docker compose ps   # Is backend running?
docker compose logs backend --tail=30
# Check DATABASE_URL in .env
```

### dbt models failing with "relation does not exist"
```bash
cd analytics
dbt run --select staging --profiles-dir ~/.dbt  # Run staging first
dbt run --profiles-dir ~/.dbt                   # Then full run
```

### Frontend shows blank page
```bash
docker compose logs frontend --tail=20  # Check nginx errors
# Verify dist/ was built: docker exec prism-frontend ls /usr/share/nginx/html
```

### Spark job fails with Java errors
```bash
# Check Java version
java -version   # Must be 11 or 17

# Increase heap
export JAVA_OPTS="-Xmx4g -Xms2g"
python -m src.pipeline.bronze
```
