# Architecture — Prism Analytics Analytics Platform

## System Overview

Prism Analytics is a cloud-native, end-to-end data engineering platform built on the Brazilian Olist e-commerce dataset. It demonstrates enterprise data engineering patterns: medallion architecture, semantic modeling, REST API serving, and a modern BI frontend.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    DATA SOURCES                          │
│  Kaggle (KaggleHub) — Olist Brazilian E-Commerce CSV    │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              SPARK ETL PIPELINE (PySpark)                │
│                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────────────┐    │
│  │  Bronze  │──▶│  Silver  │──▶│  Gold Business   │    │
│  │ Raw CSV  │   │ Cleaned  │   │  Marts (Parquet)  │    │
│  │ Parquet  │   │ Parquet  │   │                  │    │
│  └──────────┘   └──────────┘   └────────┬─────────┘    │
└─────────────────────────────────────────│───────────────┘
                                          │
                         ┌────────────────▼──────────────┐
                         │   WAREHOUSE INTEGRATION        │
                         │   SQLAlchemy → PostgreSQL      │
                         │   (Supabase)                   │
                         └────────────────┬──────────────┘
                                          │
                         ┌────────────────▼──────────────┐
                         │   dbt SEMANTIC LAYER           │
                         │   Staging views + Mart tables  │
                         │   Schema: serving.*            │
                         └────────────────┬──────────────┘
                                          │
                         ┌────────────────▼──────────────┐
                         │   FastAPI ANALYTICS API        │
                         │   16 read-only endpoints       │
                         │   SQLAlchemy sessions          │
                         │   Prometheus metrics           │
                         └────────────────┬──────────────┘
                                          │
                    ┌─────────────────────▼──────────────┐
                    │     nginx REVERSE PROXY             │
                    │  /api/* → backend:8000              │
                    │  /*     → React SPA                 │
                    └─────────────────────┬──────────────┘
                                          │
                    ┌─────────────────────▼──────────────┐
                    │   React BI DASHBOARD (Vite)         │
                    │   TanStack Query + Recharts         │
                    │   6 domain dashboards               │
                    └────────────────────────────────────┘
```

---

## Medallion Architecture

| Layer | Location | Format | Purpose |
|---|---|---|---|
| **Bronze** | `data/bronze/` | Parquet | Raw CSV preserved with original structure |
| **Silver** | `data/silver/` | Parquet | Cleaned, validated, referential integrity |
| **Gold** | `data/gold/` | Parquet | Business aggregates, mart-level granularity |
| **Serving** | PostgreSQL | Tables/Views | API-ready, indexed, dbt-materialized |

---

## Database Schema (Supabase PostgreSQL)

**Schema: `serving`**

| Table | Type | Grain | Source Mart |
|---|---|---|---|
| `fact_executive_kpis` | Table | Platform-level | Executive |
| `fact_sales_daily` | Table | Day | Sales |
| `fact_sales_monthly` | Table | Month | Sales |
| `dim_sales_revenue_by_state` | Table | State | Sales |
| `dim_customers_clv` | Table | Customer | Customers |
| `dim_customers_top_cities` | Table | City | Customers |
| `fact_customers_repeat_stats` | Table | Aggregate | Customers |
| `dim_products_performance` | Table | Product | Products |
| `dim_products_category_performance` | Table | Category | Products |
| `fact_payments_method_dist` | Table | Payment type | Finance |
| `fact_payments_installments` | Table | Installment # | Finance |
| `fact_logistics_delivery_by_state` | Table | State | Logistics |
| `fact_logistics_delivery_success_rates` | Table | Aggregate | Logistics |
| `fact_logistics_seller_shipping_perf` | Table | Seller | Logistics |

---

## API Architecture

**Base URL**: `/api/v1/`

| Domain | Endpoints | Auth |
|---|---|---|
| Health | `GET /health`, `GET /health/version` | None |
| Executive | `GET /executive/kpis` | None |
| Sales | `GET /sales/daily`, `/monthly`, `/by-state` | None |
| Customers | `GET /customers/segments`, `/top-cities`, `/repeat-stats` | None |
| Products | `GET /products/top`, `/categories` | None |
| Finance | `GET /finance/payments`, `/installments` | None |
| Logistics | `GET /logistics/performance`, `/success-rates`, `/seller-shipping` | None |
| Observability | `GET /metrics` (Prometheus) | None |

---

## Frontend Architecture

```
src/frontend/src/
├── api/client.js          ← HTTP client (16 methods)
├── hooks/useData.js        ← TanStack Query hooks (1/endpoint)
├── utils/format.js         ← Presentation formatting only
├── components/
│   ├── KPICard.jsx
│   ├── ChartCard.jsx
│   ├── States.jsx
│   ├── Sidebar.jsx
│   └── Topbar.jsx
└── pages/
    ├── Executive/
    ├── Sales/
    ├── Customers/
    ├── Products/
    ├── Finance/
    └── Logistics/
```

**Data flow**: API → TanStack Query cache → Hook → Page → Component

No business logic in the frontend. All computations are done server-side.

---

## Container Architecture

```
Docker Compose
├── prism-backend  (FastAPI + Uvicorn)
│   └── port 8000
└── prism-frontend (nginx + React dist)
    └── port 80
        └── /api/* → proxy → backend:8000
```

---

## Security Architecture

- **API**: Read-only GET endpoints. No write surface.
- **Database**: Supabase row-level security via service role key in `.env`.
- **Secrets**: Environment-variable injection at runtime (never baked into images).
- **Container**: Backend runs as non-root `appuser`.
- **CORS**: Locked to frontend origin in production.
- **Headers**: X-Frame-Options, X-Content-Type-Options, CSP via nginx.

---

## CI/CD Pipeline

```
GitHub Push to main
    ├── Job 1: Backend Tests    (pytest, 30 integration tests)
    ├── Job 2: Frontend Tests   (vitest, 15 component tests + build)
    ├── Job 3: dbt Validation   (dbt parse — model compilation check)
    └── Job 4: Docker Build     (backend + frontend image build)
         [only on main branch, after all jobs pass]
```
