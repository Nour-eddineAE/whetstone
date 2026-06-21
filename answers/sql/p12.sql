select salary 
from (select salary, DENSE_RANK() over (order by salary desc) as dr from employees) 
where dr == 2;