# Prism Analytics Platform

A **cloud-native, end-to-end data engineering platform** that ingests raw e-commerce data, processes it through a multi-layer pipeline (Bronze → Silver → Gold), loads it into a production PostgreSQL warehouse, exposes a typed REST API, and renders a real-time Business Intelligence dashboard.

---

## Architecture at a Glance

```
Raw CSV (Kaggle) → Spark ETL → Bronze → Silver → Gold Parquet
                                                       ↓
                                              PostgreSQL (Supabase)
                                                       ↓
                                               dbt Semantic Layer
                                                       ↓
                                            FastAPI Analytics API
                                                       ↓
                                          React BI Dashboard (nginx)
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Data Ingestion | Apache Spark 3.5 (PySpark) |
| Data Storage | Parquet (Bronze/Silver/Gold), PostgreSQL 15 |
| Warehouse | Supabase (PostgreSQL SaaS) |
| Semantic Layer | dbt-core 1.7 + dbt-postgres |
| API | FastAPI 0.110 + SQLAlchemy 2.x + Uvicorn |
| Frontend | React 18 + Vite + TanStack Query + Recharts |
| Serving | nginx 1.27 (SPA + reverse proxy) |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Observability | Prometheus (via prometheus-fastapi-instrumentator) |

---

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- Docker Desktop (for containerized deployment)

### Local Development

```bash
# 1. Clone and configure
git clone https://github.com/your-org/databricks-dbt-pipeline.git
cd databricks-dbt-pipeline
cp .env.example .env
# Fill in your Supabase credentials in .env

# 2. Python environment
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 3. Start API
python -m src.backend.app

# 4. Start dashboard (separate terminal)
cd src/frontend
npm install
npm run dev

# Dashboard: http://localhost:5173/
# API docs:  http://localhost:8000/api/v1/docs
```

### Production (Docker Compose)

```bash
cp .env.example .env
# Edit .env with production credentials
docker compose up -d

# Dashboard: http://localhost:80/
# API:       http://localhost:8000/api/v1/docs
```

---

## Running the Pipeline

```bash
# Bronze Layer
python -m src.pipeline.bronze

# Silver Layer
python -m src.pipeline.silver

# Gold Layer
python -m src.pipeline.gold

# Warehouse Load
python -m src.warehouse.loader

# dbt models
cd analytics && dbt run --profiles-dir ~/.dbt
```

---

## Running Tests

```bash
# Backend API tests (30 integration tests)
pytest tests/backend/ -v

# Frontend component tests (15 unit tests)
cd src/frontend && npm test
```

---

## Project Documentation

| Document | Description |
|---|---|
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Step-by-step deployment guide |
| [RUNBOOK.md](docs/RUNBOOK.md) | Operational runbook for common tasks |
| [OPERATIONS.md](docs/OPERATIONS.md) | Monitoring, alerting, and SLOs |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Full technical architecture |
| [docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) | Warehouse schema design |
| [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) | Field-level data dictionary |

---

## Dataset

Brazilian e-commerce public dataset (Olist) — 100K+ orders, 9 source tables.
- Source: [Kaggle — Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- Managed via `kagglehub` in Phase 1.

---

## License

MIT
