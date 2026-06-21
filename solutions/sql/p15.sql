-- p15 funnel. Distinct users per step, ordered along the funnel with a CASE so
-- the rows come out view -> signup -> purchase (this problem is order-sensitive).
SELECT event_type, COUNT(DISTINCT user_id) AS users
FROM events
WHERE event_type IN ('view', 'signup', 'purchase')
GROUP BY event_type
ORDER BY CASE event_type
             WHEN 'view' THEN 1
             WHEN 'signup' THEN 2
             WHEN 'purchase' THEN 3
         END;
