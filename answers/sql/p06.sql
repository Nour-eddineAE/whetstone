select dept, emp_id, name, salary 
from (select *, ROW_NUMBER() over (partition by dept order by salary desc, emp_id) as rnk from employees) 
where rnk = 1; 