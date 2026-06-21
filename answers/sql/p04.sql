select emp_id, name
from employees e
where exists (select 1 from transactions where e.emp_id = user_id)