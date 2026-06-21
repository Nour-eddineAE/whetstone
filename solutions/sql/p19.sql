-- p19 three counts in one row. COUNT(*) = all rows; DISTINCT over all columns =
-- whole-row dedup (distinct()); DISTINCT over a subset = dropDuplicates(subset).
SELECT
    (SELECT COUNT(*) FROM events) AS total,
    (SELECT COUNT(*) FROM (SELECT DISTINCT user_id, event_type, event_ts FROM events)) AS distinct_all,
    (SELECT COUNT(*) FROM (SELECT DISTINCT user_id, event_type FROM events)) AS distinct_user_event;
