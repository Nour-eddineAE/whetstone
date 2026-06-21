-- p26 group by a derived month key. strftime formats the date to 'YYYY-MM',
-- collapsing every day in a month onto the same group.
SELECT strftime(txn_date, '%Y-%m') AS month,
       COUNT(*) AS txn_count,
       SUM(amount) AS total_amount
FROM transactions
GROUP BY strftime(txn_date, '%Y-%m');
