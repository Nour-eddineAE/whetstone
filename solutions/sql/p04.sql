-- p04 semi-join via EXISTS: keep employees with >=1 transaction, no duplication.
-- A plain JOIN to transactions would emit one row per transaction (fan-out).
SELECT e.emp_id, e.name
FROM employees e
WHERE EXISTS (
    SELECT 1 FROM transactions t WHERE t.user_id = e.emp_id
);
