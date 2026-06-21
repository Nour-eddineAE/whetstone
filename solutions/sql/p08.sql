-- p08 top-N per group. You cannot filter a window function in WHERE, so compute
-- ROW_NUMBER in a subquery then filter rn <= 2 outside it.
SELECT dept, emp_id, name, salary, rn
FROM (
    SELECT dept, emp_id, name, salary,
           ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC, emp_id) AS rn
    FROM employees
) ranked
WHERE rn <= 2;
