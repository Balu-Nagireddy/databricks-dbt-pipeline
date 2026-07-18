select * from {{ source('serving', 'dim_customers_clv') }}
