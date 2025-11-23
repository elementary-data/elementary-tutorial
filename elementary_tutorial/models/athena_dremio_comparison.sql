with athena_latest_invocation as (
    select invocation_id from {{source('athena_elementary', 'dbt_invocations')}}
    order by run_completed_at desc
    limit 1
),

    athena_latest_run_results as (
    select * from {{source('athena_elementary', 'dbt_run_results')}}
    where invocation_id in (select invocation_id from athena_latest_invocation)
),

    dremio_latest_invocation as (
    select invocation_id from {{ref('dbt_invocations')}}
    order by run_completed_at desc
    limit 1
),

    dremio_latest_run_results as (
    select * from {{ref('dbt_run_results')}}
    where invocation_id in (select invocation_id from dremio_latest_invocation)
),

    final as (
        select 
            athena_latest_run_results.unique_id as unique_id,
            athena_latest_run_results.invocation_id as athena_invocation_id,
            dremio_latest_run_results.invocation_id as dremio_invocation_id,
            athena_latest_run_results.status as athena_status,
            dremio_latest_run_results.status as dremio_status,
            athena_latest_run_results.execution_time as athena_execution_time,
            dremio_latest_run_results.execution_time as dremio_execution_time,
            case when athena_latest_run_results.execution_time < dremio_latest_run_results.execution_time then 'athena' else 'dremio' end as faster_warehouse
        from athena_latest_run_results
        full outer join dremio_latest_run_results on athena_latest_run_results.unique_id = dremio_latest_run_results.unique_id
    )

select * from final