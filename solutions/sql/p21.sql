-- p21 conditional aggregation (a pivot built by hand): one SUM(CASE ...) per band.
-- CASE turns each row into a 0/1 flag; SUM counts the 1s within each dept group.
SELECT dept,
       SUM(CASE WHEN salary < 60000 THEN 1 ELSE 0 END) AS low,
       SUM(CASE WHEN salary >= 60000 AND salary < 90000 THEN 1 ELSE 0 END) AS mid,
       SUM(CASE WHEN salary >= 90000 THEN 1 ELSE 0 END) AS high
FROM employees
GROUP BY dept;
