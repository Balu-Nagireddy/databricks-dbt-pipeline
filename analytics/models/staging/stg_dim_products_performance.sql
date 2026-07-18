select * from {{ source('serving', 'dim_products_performance') }}
