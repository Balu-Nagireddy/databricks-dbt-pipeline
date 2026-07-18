select * from {{ source('serving', 'fact_payments_method_dist') }}
