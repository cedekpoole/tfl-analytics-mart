-- question: which tube lines had the highest disrupted snapshot percentage?
-- grain: one row per tube line across the collected period
-- input: mart_line_status_counts


select
    line_id,
    line_name,
    sum(disrupted_snapshot_count) as disrupted_snapshots,
    sum(snapshot_count) as total_snapshots,
    round(100 * safe_divide(sum(disrupted_snapshot_count), sum(snapshot_count)), 2) as disrupted_snapshot_pct
from `tfl-analytics-mart.dbt_cameron.mart_line_status_counts`
group by
    line_id,
    line_name
order by
    disrupted_snapshot_pct desc,
    disrupted_snapshots desc;