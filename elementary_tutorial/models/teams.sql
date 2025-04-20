{{
    config(
        materialized='table'
    )
}}

with players as (
    select * from {{ source('guy_playground', 'players') }}
)

select 
    team,
    min(age) as youngest_player,
    max(age) as oldest_player,
    avg(age) as average_age,
    case when sum(case when shirt_number = 10 then 1 else 0 end) > 0 then true else false end as ten_shirt_worn,
    count(*) as player_count
from players
group by team