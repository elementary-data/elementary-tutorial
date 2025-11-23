select * from {{source('athena', 'orders_v2_athena')}}
where order_date > select max(order_date) from {{source('dremio-s3', 'orders_validation_v2')}}
and user_id > 90