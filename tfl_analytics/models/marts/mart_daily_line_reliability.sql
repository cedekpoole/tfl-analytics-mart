with line_status_snapshots as (

    select *
    from {{ ref('fct_line_status_snapshots') }}

),

daily_line_reliability as (

    select
        snapshot_date,
        line_id,
        line_name,
        count(*) as total_snapshots,
        countif(is_good_service) as good_service_snapshots,
        countif(is_disrupted) as disrupted_snapshots,
        round(100 * safe_divide(countif(is_good_service), count(*)), 2) as good_service_pct,
        round(100 * safe_divide(countif(is_disrupted), count(*)), 2) as disrupted_pct
    from line_status_snapshots
    group by
        snapshot_date,
        line_id,
        line_name

)

select *
from daily_line_reliability