# Operations Guide — Prism Analytics Analytics Platform

## Monitoring

### Health Endpoints

| Endpoint | Description | Expected Response |
|---|---|---|
| `GET /api/v1/health` | API + DB liveness | `{"status":"ok","database":"connected"}` |
| `GET /api/v1/health/version` | Version metadata | `{"version":"1.0.0"}` |
| `GET /metrics` | Prometheus metrics | Prometheus text format |
| `GET /nginx-health` | nginx liveness | `ok` |

### Prometheus Metrics

The backend exposes Prometheus metrics at `GET /metrics`. Key metrics:

| Metric | Description |
|---|---|
| `http_requests_total` | Total requests by method, handler, status |
| `http_request_duration_seconds` | Request duration histogram |
| `http_request_size_bytes` | Request body sizes |
| `http_response_size_bytes` | Response body sizes |

**Prometheus scrape config example:**
```yaml
scrape_configs:
  - job_name: prism-backend
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: /metrics
    scrape_interval: 15s
```

### X-Process-Time Header

Every response includes `X-Process-Time: <ms>` from the `TimingMiddleware`. Use this in nginx access logs for SLA tracking.

---

## Service Level Objectives (SLOs)

| SLO | Target |
|---|---|
| API availability | ≥ 99.5% uptime |
| p95 response time | < 500ms |
| p99 response time | < 2000ms |
| Error rate | < 1% |
| Data pipeline freshness | Daily refresh |

---

## Alerting Recommendations

Configure Prometheus AlertManager rules for:

```yaml
groups:
  - name: prism
    rules:
      - alert: APIDown
        expr: up{job="prism-backend"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Prism Analytics API is down"

      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Error rate above 5%"

      - alert: SlowResponses
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "p95 latency above 500ms"
```

---

## Logging

The platform uses structured Python `logging` via `src.common.logging`:

- **Format**: `TIMESTAMP [LEVEL] module: message`
- **Handlers**: Console (stdout) — easily ingested by Docker logging drivers
- **Log levels**: `INFO` in production, `DEBUG` in development

### Querying Logs

```bash
# All ERROR logs from backend container
docker compose logs backend 2>&1 | grep "\[ERROR\]"

# Request logs by path
docker compose logs backend 2>&1 | grep "/api/v1/executive"

# Last 1 hour of logs
docker compose logs --since=1h backend
```

---

## Backup and Recovery

### Database (Supabase)
- Supabase provides automatic daily backups (Point-in-Time Recovery on Pro plan)
- Manual backup:
  ```bash
  pg_dump "$DATABASE_URL" -n serving > backup_serving_$(date +%Y%m%d).sql
  ```

### Pipeline Data (Parquet)
- Bronze/Silver/Gold Parquet files live in `data/` (excluded from Git)
- Backup strategy: sync to object storage (S3/GCS) after each pipeline run
- Recovery: re-run `python -m src.pipeline.bronze` → silver → gold → loader

### Configuration
- `.env` must be backed up securely (password manager, secrets vault, or CI secrets)
- All code is in Git — no additional backup needed

---

## Security

### Environment Variables
- Secrets are loaded from `.env` at runtime
- `.env` is in `.gitignore` — never committed
- In CI/CD, secrets are injected as GitHub Actions secrets

### CORS Policy
- Production: origins locked to specific frontend domain (update `CORS_ORIGINS` in `src/backend/config.py`)
- Development: localhost origins only

### API Design
- All endpoints are read-only (`GET`)
- No authentication required (internal network deployment assumed)
- For public exposure: add OAuth2/API key middleware before deployment

### Dependency Scanning
- `npm audit` runs automatically on `npm install`
- Review `pip-audit` output before production deploys:
  ```bash
  pip install pip-audit
  pip-audit -r requirements.txt
  ```

### Docker Security
- Backend container runs as non-root (`appuser`)
- Frontend served by official nginx alpine image
- No secrets in Docker images (passed via env_file at runtime)

---

## Capacity Planning

| Service | CPU | Memory | Notes |
|---|---|---|---|
| Backend (Uvicorn 2 workers) | 0.5–1 vCPU | 256–512 MB | Scale workers for higher throughput |
| Frontend (nginx) | < 0.1 vCPU | 32–64 MB | Static serving, very lightweight |
| Spark pipeline | 2–4 vCPU | 4–8 GB | Run offline, not as a service |
| PostgreSQL | Supabase managed | Supabase managed | Connection pool via pgbouncer |
