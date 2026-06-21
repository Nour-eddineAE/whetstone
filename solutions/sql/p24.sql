-- p24 HAVING filters GROUPS after aggregation (WHERE filters rows before it).
-- Both conditions are on aggregates, so both belong in HAVING.
SELECT dept, COUNT(*) AS headcount, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept
HAVING COUNT(*) > 5 AND AVG(salary) > 70000;
