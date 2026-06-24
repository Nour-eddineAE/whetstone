with formatted_month as (
    select substr(cast(txn_date as varchar), 1, 7) as month, 
  			amount
    from transactions
)
select month, 
		count(*) as txn_count,
		sum(amount) as total_amount
from formatted_month
group by month; 