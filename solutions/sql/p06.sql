-- p06 top earner per dept. ROW_NUMBER gives exactly one row per partition;
-- the emp_id tiebreak makes it deterministic when salaries tie.
SELECT dept, emp_id, name, salary
FROM (
    SELECT dept, emp_id, name, salary,
           ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC, emp_id) AS rn
    FROM employees
) ranked
WHERE rn = 1;
