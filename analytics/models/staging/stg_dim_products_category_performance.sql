select * from {{ source('serving', 'dim_products_category_performance') }}
