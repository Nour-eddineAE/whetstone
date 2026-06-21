-- p16 median per user. DuckDB's median() is the exact interpolated 50th
-- percentile (average of the two middle rows for even counts).
SELECT user_id, median(amount) AS median_amount
FROM transactions
GROUP BY user_id;
