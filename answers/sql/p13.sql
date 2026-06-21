select user_id, event_type, event_ts
from (select user_id, event_type, event_ts, ROW_NUMBER() over (partition by user_id, event_type order by event_ts desc) as rn from events) 
where rn = 1; 