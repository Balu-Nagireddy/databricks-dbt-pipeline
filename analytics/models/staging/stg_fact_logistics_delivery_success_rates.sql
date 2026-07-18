select * from {{ source('serving', 'fact_logistics_delivery_success_rates') }}
