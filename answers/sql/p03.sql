select emp_id, name
from employees m
where not exists (select 1 from employees e where e.manager_id = m.emp_id);