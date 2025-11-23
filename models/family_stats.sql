{{
    config(
        materialized='table'
    )
}}

with family_members as (
    select * from {{ ref('family_members') }}
)

select 
    last_name,
    count(*) as member_count,
    max(age) as oldest_member,
    min(age) as youngest_member,
    sum(case when gender = 'Female' then 1 else 0 end) as female_count,
    sum(case when gender = 'Male' then 1 else 0 end) as male_count
from family_members
group by last_name
