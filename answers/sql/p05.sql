select dept, sum(amount) as total_amount 
from employees e
join transactions t on e.emp_id = t.user_id
group by dept;