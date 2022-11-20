with customers as (

    select * from {{ ref('stg_customers') }}

),

orders as (

    select * from {{ ref('stg_orders') }}

),

payments as (

    select * from {{ ref('stg_payments') }}

),

signups as (

    select * from {{ ref('stg_signups') }}
),

customer_orders as (

        select
        customer_id,

        min(order_date) as first_order,
        max(order_date) as most_recent_order,
        count(order_id) as number_of_orders
    from orders

    group by customer_id

),

customer_payments as (

    select
        orders.customer_id,
        sum(amount) as total_amount

    from payments

    left join orders on
         payments.order_id = orders.order_id

    group by orders.customer_id

),

final as (

    select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order,
        customer_orders.most_recent_order,
        case
            when customer_orders.number_of_orders is null then 0
            else customer_orders.number_of_orders
        end as number_of_orders,
        customer_payments.total_amount as customer_lifetime_value,
        signups.customer_email,
        {% if elementary.get_config_var('anomalies') %}
            signups.customer_email as customer_email_2,
        {% endif %}
        signups.signup_date

    from customers

    left join customer_orders
        on customers.customer_id = customer_orders.customer_id

    left join customer_payments
        on  customers.customer_id = customer_payments.customer_id

    left join signups
        on customers.customer_id = signups.customer_id

)

select * from final
