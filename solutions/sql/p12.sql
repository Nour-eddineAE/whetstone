-- p12 second highest distinct salary. MAX below the global MAX naturally
-- collapses ties at the top, and returns NULL if there is no runner-up.
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
