-- p22 self-join: the same table twice, employee e to manager m via e.manager_id.
-- Employees with a NULL manager_id simply don't match (inner join drops them).
SELECT e.emp_id, e.name, e.salary, m.salary AS manager_salary
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary;
