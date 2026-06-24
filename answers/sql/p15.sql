select event_type, count(distinct user_id) as users
from events
where event_type in ('view', 'signup', 'purchase')
group by event_type
order by case event_type
			when 'view' then 1
            when 'signup' then 2
            when 'puchase' then 3
            end
;  