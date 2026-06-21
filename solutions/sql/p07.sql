-- p07 RANK vs DENSE_RANK over the same partition/order.
-- RANK skips numbers after a tie (1,1,3); DENSE_RANK is gapless (1,1,2).
SELECT emp_id, dept, salary,
       RANK()       OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk,
       DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dense_rnk
FROM employees;
