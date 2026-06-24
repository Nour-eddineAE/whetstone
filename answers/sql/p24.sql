select dept, 
		count(*) as headcount, 
        AVG(salary) as avg_salary 
from employees 
group by dept
having headcount > 5
		and avg_salary > 70000; 
