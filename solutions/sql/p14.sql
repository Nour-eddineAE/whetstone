-- p14 gaps-and-islands. One login date per user/day, then subtract the row
-- number (in days): consecutive dates collapse to the same anchor date `grp`.
-- Count per group = streak length; take the max per user.
WITH days AS (
    SELECT DISTINCT user_id, CAST(event_ts AS DATE) AS dt
    FROM events
    WHERE event_type = 'login'
),
grouped AS (
    SELECT user_id, dt,
           dt - CAST(ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY dt) AS INTEGER) AS grp
    FROM days
),
streaks AS (
    SELECT user_id, grp, COUNT(*) AS streak
    FROM grouped
    GROUP BY user_id, grp
)
SELECT user_id, MAX(streak) AS max_streak
FROM streaks
GROUP BY user_id;
