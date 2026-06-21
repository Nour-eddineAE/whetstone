-- p11 frame trap. With ORDER BY the default frame is RANGE UNBOUNDED PRECEDING
-- ... CURRENT ROW => running. Without ORDER BY the frame is the whole partition
-- => grand total. Same SUM(amount), two different results.
SELECT user_id, txn_id, txn_date,
       SUM(amount) OVER (
           PARTITION BY user_id ORDER BY txn_date, txn_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total,
       SUM(amount) OVER (PARTITION BY user_id) AS grand_total
FROM transactions;
