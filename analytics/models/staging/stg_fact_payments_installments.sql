select * from {{ source('serving', 'fact_payments_installments') }}
