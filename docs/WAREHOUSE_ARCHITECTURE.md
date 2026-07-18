# Warehouse Serving Layer Architecture

This document defines the architecture of the PostgreSQL serving layer on Supabase.

## 1. Architectural Pattern

The PostgreSQL warehouse operates strictly as a **Serving Layer**, not a Processing Layer. All heavy computing, windowing, and data cleaning are completed inside the PySpark Bronze, Silver, and Gold pipelines.

```
[PySpark Compute Engine] ──(Parquet files)──► [PostgreSQL serving schema] ──► [dbt Semantic Layer / APIs]
```

This separation guarantees:
1. **Low Compute Overhead**: PostgreSQL CPU and RAM are reserved for query serving (indexes, joins, and aggregates).
2. **Simplified Scaling**: Computing can scale horizontally with Spark, while serving capacity scales via database read replicas.
3. **Idempotency**: All ingestion steps are reproducible and non-destructive.

## 2. Ingestion & Idempotency Strategy

To ensure pipelines can be re-run safely at any time:
- **Full Refresh Ingestion**:
  1. A target table is loaded via `TRUNCATE TABLE serving.table_name;`.
  2. The new Gold Parquet payload is written using standard batch inserts/copy.
  3. Committed inside a single transaction to prevent incomplete states.
- **Incremental Enablement**:
  - Each table includes an ingestion metadata column: `_loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP`.
  - In future phases, incremental reads can query `WHERE _loaded_at > :last_load_timestamp` to support delta syncs.

## 3. Serving Consumers

The serving layer schemas and indexes are specifically optimized for:
- **dbt Core (Semantic Modeling)**: Tables use consistent primary-foreign key structures allowing dbt to easily map metrics and dimensions.
- **FastAPI REST API**: High-priority endpoints are backed by composite B-Tree indexes, allowing sub-second reads for customer profiles, top-selling products, and logistics indicators.
