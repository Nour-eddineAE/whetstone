select user_id, txn_id, txn_date, 
	SUM(amount) over (partition by user_id order by txn_date, txn_id rows between unbounded preceding and current row) as running_total, 
    SUM(amount) over (partition by user_id) grand_total
from transactions; 