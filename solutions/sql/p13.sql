-- p13 dedup keep-latest. MAX(event_ts) per (user, type) collapses the duplicate
-- and repeated rows to the most recent timestamp.
SELECT user_id, event_type, MAX(event_ts) AS event_ts
FROM events
GROUP BY user_id, event_type;
