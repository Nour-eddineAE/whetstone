-- p10 month-over-month. Aggregate to monthly totals first, THEN LAG across
-- months. LAG of the first month is NULL -> mom_change NULL there too.
WITH monthly AS (
    SELECT strftime(txn_date, '%Y-%m') AS month, SUM(amount) AS monthly_amount
    FROM transactions
    GROUP BY 1
)
SELECT month,
       monthly_amount,
       LAG(monthly_amount) OVER (ORDER BY month) AS prev_amount,
       monthly_amount - LAG(monthly_amount) OVER (ORDER BY month) AS mom_change
FROM monthly;
