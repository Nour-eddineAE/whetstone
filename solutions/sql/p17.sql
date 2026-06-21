-- p17 salary bands via CASE, then group and count.
SELECT band, COUNT(*) AS num_employees
FROM (
    SELECT CASE
               WHEN salary < 60000 THEN 'low'
               WHEN salary < 90000 THEN 'mid'
               ELSE 'high'
           END AS band
    FROM employees
) b
GROUP BY band;
