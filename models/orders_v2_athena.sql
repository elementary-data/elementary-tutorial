{{ config(
    table_type = 'iceberg',
    materialized = 'table'
) }}
select * from {{ref('orders_validation')}}