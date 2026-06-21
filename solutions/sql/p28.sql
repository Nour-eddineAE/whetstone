-- p28 the SQL way to pivot: one SUM(CASE ...) column per event type. (Spark has
-- a native .pivot() for this; see the PySpark reference.)
SELECT user_id,
       SUM(CASE WHEN event_type = 'view'     THEN 1 ELSE 0 END) AS view,
       SUM(CASE WHEN event_type = 'signup'   THEN 1 ELSE 0 END) AS signup,
       SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchase,
       SUM(CASE WHEN event_type = 'click'    THEN 1 ELSE 0 END) AS click,
       SUM(CASE WHEN event_type = 'login'    THEN 1 ELSE 0 END) AS login
FROM events
GROUP BY user_id;
