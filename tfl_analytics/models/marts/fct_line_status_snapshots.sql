with line_statuses as (

    select *
    from {{ ref('stg_tfl_line_statuses') }}

),

final as (

    select
        utc_fetched_at,
        date(utc_fetched_at) as snapshot_date,
        source_url,
        line_id,
        line_name,
        status_description,
        status_description = 'Good Service' as is_good_service,
        status_description != 'Good Service' as is_disrupted
    from line_statuses

)

select *
from final