select dept, emp_id, name, salary, rn 
from (select dept, emp_id, name, salary, ROW_NUMBER() over (partition by dept order by salary desc, emp_id) as rn from employees) 
where rn < 3; 