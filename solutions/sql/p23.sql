-- p23 self-join for pairs. a.emp_id < b.emp_id does two jobs: drops self-pairs
-- (a = b) and keeps only one of each mirrored pair (1,2) without also (2,1).
SELECT a.emp_id AS emp_id1, b.emp_id AS emp_id2, a.dept
FROM employees a
JOIN employees b ON a.dept = b.dept AND a.emp_id < b.emp_id;
