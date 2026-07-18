select * from {{ source('serving', 'fact_customers_repeat_stats') }}
