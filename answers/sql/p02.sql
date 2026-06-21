select emp_id, name, dept_id
from employees e left join departments d on e.dept = d.dept_name; 