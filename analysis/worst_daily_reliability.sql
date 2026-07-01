-- question: Which Tube lines had the lowest daily Good Service percentage?
-- grain: one row per tube line per snapshot date
-- input: mart_daily_line_reliability

select
    snapshot_date,
    line_id,
    line_name,
    total_snapshots,
    good_service_snapshots,
    disrupted_snapshots,
    good_service_pct,
    disrupted_pct
from `tfl-analytics-mart.dbt_cameron.mart_daily_line_reliability`
order by
    good_service_pct asc,
    disrupted_pct desc,
    total_snapshots desc,
    line_name;