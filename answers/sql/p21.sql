select dept, 
		count(case when salary < 60000 then emp_id end) as low, 
		count(case when salary between 60000 and 89999 then emp_id end) as mid, 
        count(case when salary >= 90000 then emp_id end) as high
from employees
group by dept; 