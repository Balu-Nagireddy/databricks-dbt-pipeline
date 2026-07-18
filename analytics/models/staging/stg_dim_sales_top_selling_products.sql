select * from {{ source('serving', 'dim_sales_top_selling_products') }}
