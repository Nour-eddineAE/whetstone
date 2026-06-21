select user_id, max(streak) as max_streak 
from (
    select user_id, count(*) as streak
    from (
        select distinct user_id, event_type, 
            STRFTIME(event_ts, '%Y-%m-%d') as event_date, 
            row_number() over (partition by user_id, event_type order by STRFTIME(event_ts, '%Y-%m-%d')) as rn 
        from events 
        where event_type = 'login'
    ) 
    group by user_id, CAST(event_date AS DATE) - rn * INTERVAL '1' DAY
)
group by user_id;