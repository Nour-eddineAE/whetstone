-- p02 left join: keep every employee; dept_id is NULL when dept has no match.
SELECT e.emp_id, e.name, d.dept_id
FROM employees e
LEFT JOIN departments d ON e.dept = d.dept_name;
