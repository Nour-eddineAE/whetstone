select emp_id, 
	case when manager_id is not NULL then manager_id 
    else -1 end as manager_id_filled
from employees; 