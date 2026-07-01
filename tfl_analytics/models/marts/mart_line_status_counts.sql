-- purpose: count how often each tube line appeared in each status across the entire period
-- grain: one row per tube line and status description
-- input: fct_line_status_snapshots

with line_status_snapshots as (

    select *
    from {{ ref('fct_line_status_snapshots') }}

),

status_counts as (

    select
        line_id,
        line_name,
        status_description,
        count(*) as snapshot_count,
        countif(is_disrupted) as disrupted_snapshot_count,
        countif(is_good_service) as good_service_snapshot_count
    from line_status_snapshots
    group by
        line_id,
        line_name,
        status_description

)

select *
from status_counts