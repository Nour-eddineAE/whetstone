with totals as(
    select dept, SUM(salary) as total_salary
    from employees
    group by dept
), 
ranked as (
    select dept, 
        total_salary,
        rank() over (order by total_salary desc) as rnk
    from totals
)
select * 
from ranked 
where rnk <= 3; 
    