-- depends_on: {{ ref('orders_validation') }}

{% if elementary.get_config_var('anomalies') %}
    with source as (
        select * from {{ ref('orders_validation') }}
    ),

{% else %}
    with source as (
        select * from {{ ref('orders_training') }}
    ),
{% endif %}

renamed as (

    select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

    from source

)

select * from renamed
