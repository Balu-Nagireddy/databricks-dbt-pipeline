select * from {{ source('serving', 'fact_logistics_delivery_by_state') }}
