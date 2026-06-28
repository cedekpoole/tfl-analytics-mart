with source as (

    select
        utc_fetched_at,
        source_url,
        data
    from {{ source('raw_tfl', 'line_status_snapshots') }}

),

line_statuses as (

    select
        source.utc_fetched_at,
        source.source_url,
        json_value(line, '$.id') as line_id,
        json_value(line, '$.name') as line_name,
        json_value(line, '$.lineStatuses[0].statusSeverityDescription') as status_description
    from source
    cross join unnest(json_query_array(source.data)) as line

)

select *
from line_statuses