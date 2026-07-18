select * from {{ source('serving', 'fact_sales_weekly') }}
