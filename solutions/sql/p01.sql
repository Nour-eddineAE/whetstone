-- p01 inner join: only employees whose dept matches a department row.
-- INNER drops 'Operations' employees (no department row) and any dept with no employees.
SELECT e.emp_id, e.name, d.dept_id
FROM employees e
JOIN departments d ON e.dept = d.dept_name;
