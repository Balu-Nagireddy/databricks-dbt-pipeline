# Silver Layer Data Quality Report

This report documents input/output row metrics, referential integrity violations, and null value handling executed during Silver transforms.

## Data Validation & Lineage Summary

| Dataset Name | Input Rows (Bronze) | Output Rows (Silver) | Rejected Rows | Referential Violations | Nulls Imputed |
| :--- | :---: | :---: | :---: | :---: | :---: |
| customers | 99,441 | 99,441 | 0 | 0 | 0 |
| geolocation | 738,332 | 738,332 | 0 | 0 | 0 |
| orders | 99,441 | 99,441 | 0 | 0 | 0 |
| order_items | 112,650 | 112,650 | 0 | 0 | 0 |
| order_payments | 103,886 | 103,886 | 0 | 0 | 0 |
| order_reviews | 104,071 | 99,224 | 4,847 | 3 | 0 |
| products | 32,951 | 32,951 | 0 | 0 | 2 |
| sellers | 3,095 | 3,095 | 0 | 0 | 0 |
| category_translation | 71 | 71 | 0 | 0 | 0 |

## Business Transformation Rules Applied
1. **Customers**: Standardized states to uppercase, cities to lowercase. Dropped null primary keys.
2. **Orders**: Standardized status. Calculated delivery duration using difference between creation and carrier delivery timestamps.
3. **Products**: Imputed missing physical characteristics (dimensions, photos count, weight) to 0. Joined English translation categories.
4. **Payments**: Normalised type to lowercase. Replaced missing value parameters with defaults. Segregated payments lacking valid orders.
5. **Reviews**: Cleaned text spacing (new line and tabs removals) from comment fields. Removed rows with missing review scores.