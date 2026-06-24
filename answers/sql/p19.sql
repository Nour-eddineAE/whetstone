SELECT
    (SELECT COUNT(*) FROM events) AS total_rows,
    (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM events)) AS distinct_rows,
    (SELECT COUNT(*) FROM (SELECT DISTINCT user_id, event_type FROM events)) AS distinct_pair;
    
    
    
    