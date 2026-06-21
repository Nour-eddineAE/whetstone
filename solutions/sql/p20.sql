-- p20 null handling. COALESCE returns the first non-NULL, so NULL managers -> -1.
SELECT emp_id, COALESCE(manager_id, -1) AS manager_id_filled
FROM employees;
