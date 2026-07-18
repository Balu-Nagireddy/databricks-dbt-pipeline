# Gold Layer Business Data Quality Report

This report documents business checks, aggregations, and metrics validations completed at the Gold Analytical Layer.

## Quality Gate Validation Checks

| Validation Test | Status | Details |
| :--- | :---: | :--- |
| Product ID Uniqueness in Product Performance | `PASS` | Total products: 32951, Unique: 32951 |
| No Null Lifetime Value in Customer Mart | `PASS` | Null value count: 0 |
| No Null Total Value in Payment Distribution | `PASS` | Null payment value count: 0 |

- **Final Acceptance Rate**: **100.00%**

## Row Summary for Primary Analytical Marts

| Mart Dataset | Row Count |
| :--- | :---: |
| daily_sales | 616 |
| weekly_sales | 95 |
| monthly_sales | 24 |
| yearly_sales | 3 |
| revenue_by_state | 27 |
| revenue_by_city | 4,300 |
| revenue_by_seller | 3,095 |
| revenue_by_category | 74 |
| top_selling_products | 32,951 |
| average_order_value | 1 |
| customer_lifetime_value | 95,420 |
| top_customer_cities | 4,310 |
| repeat_customer_stats | 2 |
| product_performance | 32,951 |
| category_performance | 74 |
| payment_method_distribution | 5 |
| payment_installments_analysis | 24 |
| delivery_by_state | 27 |
| delivery_success_rates | 1 |
| seller_shipping_performance | 3,095 |
| executive_kpis | 1 |

## Business Rules Applied
1. **Unique Domain Keys**: Checked that product-level and customer-level metrics contain no key collisions.
2. **Completeness Checks**: Enforced no null values in financial aggregations or calculated customer value.