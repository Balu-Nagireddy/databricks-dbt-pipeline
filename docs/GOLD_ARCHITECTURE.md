# Gold Layer Architecture Documentation

This document explains the design, metrics, transformations, and execution patterns of the Gold Analytical Layer.

## 1. Architectural Overview

The Gold layer transforms clean operational datasets (from the Silver layer) into analytics-ready business marts. Each mart is structured around a single business domain following SOLID principles.

```
data/
└── gold/
    ├── sales/      # Daily/Weekly/Monthly metrics, state/city stats, AOV
    ├── customers/  # Lifetime value, Segmentation, City distributions
    ├── products/   # Performance, Best/worst sellers, Category rankings
    ├── finance/    # Payment types, Installments distributions
    ├── logistics/  # Delivery durations, Late order rates, Seller transit times
    └── executive/  # Consolidated Executive KPI Dashboard stats
```

## 2. Business Mart Details & Metrics

### Sales Mart (`sales/`)
- **Daily/Weekly/Monthly/Yearly Sales**: Temporal aggregations to monitor revenue trends.
- **Revenue by Region**: Aggregated sales values and order counts grouped by customer city and state.
- **Average Order Value (AOV)**: Average amount spent per transaction.

### Customer Mart (`customers/`)
- **Customer Lifetime Value (CLV)**: Sum of all order values grouped by unique customer identifier.
- **Customer Segmentation**:
  - `VIP`: Lifetime spend > $500.00
  - `High Value`: Lifetime spend > $150.00
  - `Standard`: Lifetime spend <= $150.00
- **Repeat Buyer Index**: Identifies if a customer has ordered more than once.

### Product Mart (`products/`)
- **Product Performance**: Total sales revenue and unit counts by product.
- **Category Performance**: Sales performance across translated English category names.

### Finance Mart (`finance/`)
- **Payment Method Distribution**: Total and average transaction value by payment type.
- **Installment Analysis**: Financial impact of payment installments.

### Logistics Mart (`logistics/`)
- **Delivery Success Rate**: Rate of completed deliveries.
- **Late Delivery Ratio**: Percentage of shipments delivered after the estimated date.
- **Shipping Time by State**: Average delivery duration (in days) grouped by customer location.

### Executive Mart (`executive/`)
- **KPI Metrics**: Single-row summary table containing high-level indicators (Total Revenue, Orders, Customers, Products, Sellers, Avg Delivery Time, Avg Review Score).

## 3. Data Quality & Gateway Validation

The Business Validation Gateway (`quality.py`) validates:
1. **Uniqueness**: Confirms unique primary keys for analytical marts.
2. **Completeness**: Checks that core metrics (such as lifetime value or transaction counts) contain no nulls.
3. **Report Output**: Outputs results directly into `docs/GOLD_DATA_QUALITY.md`.
