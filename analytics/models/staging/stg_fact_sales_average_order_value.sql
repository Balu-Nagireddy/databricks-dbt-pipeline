select * from {{ source('serving', 'fact_sales_average_order_value') }}
