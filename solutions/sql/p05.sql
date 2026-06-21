-- p05 revenue per dept. Join ONE child table (transactions) then aggregate.
-- Adding a join to events here would duplicate each txn per event = fan-out.
SELECT e.dept, SUM(t.amount) AS total_amount
FROM employees e
JOIN transactions t ON t.user_id = e.emp_id
GROUP BY e.dept;
