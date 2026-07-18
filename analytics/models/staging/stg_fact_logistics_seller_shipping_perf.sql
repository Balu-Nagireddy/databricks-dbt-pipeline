select * from {{ source('serving', 'fact_logistics_seller_shipping_perf') }}
