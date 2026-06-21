-- p09 running total per user. The frame ROWS UNBOUNDED PRECEDING ... CURRENT ROW
-- makes it cumulative; txn_id tiebreak keeps the order deterministic.
SELECT user_id, txn_id, txn_date, amount,
       SUM(amount) OVER (
           PARTITION BY user_id
           ORDER BY txn_date, txn_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM transactions;
