select * from {{ source('serving', 'dim_customers_top_cities') }}
