-- depends_on: {{ ref('customers_validation') }}

{% if elementary.get_config_var('anomalies') %}
    with source as (
        select * from {{ ref('customers_validation') }}
    ),

{% else %}
    with source as (
        select * from {{ ref('customers_training') }}
    ),
{% endif %}

renamed as (

    select
        id as customer_id,
        first_name,
        last_name

    from source

)

select * from renamed
