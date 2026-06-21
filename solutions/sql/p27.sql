-- p27 correlated subquery: the inner query re-runs per outer row, referencing
-- e.dept, so each employee is compared to their OWN department's average.
SELECT e.emp_id, e.name, e.dept, e.salary
FROM employees e
WHERE e.salary > (
    SELECT AVG(d.salary) FROM employees d WHERE d.dept = e.dept
);
