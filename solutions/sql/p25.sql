-- p25 multi-step with CTEs: aggregate first, then rank the aggregate, then filter.
-- You can't rank in the same step you aggregate, so build it up in layers.
WITH dept_totals AS (
    SELECT dept, SUM(salary) AS total_salary
    FROM employees
    GROUP BY dept
),
ranked AS (
    SELECT dept, total_salary,
           RANK() OVER (ORDER BY total_salary DESC) AS rnk
    FROM dept_totals
)
SELECT dept, total_salary, rnk
FROM ranked
WHERE rnk <= 3;
