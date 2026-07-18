select * from {{ source('serving', 'dim_sales_revenue_by_city') }}
