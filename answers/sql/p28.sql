select user_id, 
	count(case when event_type = 'view' then user_id end) as view, 
    count(case when event_type = 'signup' then user_id end) signup, 
    count(case when event_type = 'purchase' then user_id end) purchase, 
    count(case when event_type = 'click' then user_id end) click, 
    count(case when event_type = 'login' then user_id end) login
from events
group by user_id;