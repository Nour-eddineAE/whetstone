select band, count(band) as num_employees
from (
    select case when salary < 60000 then 'low' 
             	when salary between 60000 and 89999 then 'mid'
            	when salary >= 90000 then 'high' end
            as band
	from employees
)
group by band
having band is not NULL; 