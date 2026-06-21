
select emp_id, dept, salary, 
	RANK() over (partition by dept order by salary desc) as rnk,
    DENSE_RANK() over (partition by dept order by salary desc) as dense_rnk
from employees; 