-- question: what is the latest collected status for each Tube line?
-- grain: one row per Tube line
-- input: fct_line_status_snapshots

with ranked_statuses as (

    select
        utc_fetched_at,
        line_id,
        line_name,
        status_description,
        is_good_service,
        is_disrupted,
        -- window function - number rows within each tube line
        row_number() over (
            partition by line_id
            order by utc_fetched_at desc
        ) as row_number
    from `tfl-analytics-mart.dbt_cameron.fct_line_status_snapshots`

)

select
    utc_fetched_at,
    line_id,
    line_name,
    status_description,
    is_good_service,
    is_disrupted
from ranked_statuses
where row_number = 1
order by line_name;