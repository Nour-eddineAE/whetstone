-- p03 anti-join via NOT EXISTS (NULL-safe). An employee is a leaf if no other
-- row lists them as manager_id. NOT IN would break here because manager_id
-- contains NULLs (NULL makes NOT IN return UNKNOWN for every row).
SELECT e.emp_id, e.name
FROM employees e
WHERE NOT EXISTS (
    SELECT 1 FROM employees m WHERE m.manager_id = e.emp_id
);
