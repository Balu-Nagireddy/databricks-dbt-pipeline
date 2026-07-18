select * from {{ source('serving', 'fact_executive_kpis') }}
