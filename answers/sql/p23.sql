select e1.emp_id as emp_id1,e2.emp_id as emp_id2, e1.dept 
from employees e1
join employees e2 on e1.emp_id < e2.emp_id and e1.dept = e2.dept; 
