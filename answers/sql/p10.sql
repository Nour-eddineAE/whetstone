with monthly as (
    select SUBSTR(CAST(txn_date AS VARCHAR), 1, 7)  as month, 
        SUM(amount) as monthly_amount
    from transactions
    group by SUBSTR(CAST(txn_date AS VARCHAR), 1, 7)
)
select 	month, 
		monthly_amount , 
		LAG(monthly_amount) over (order by month) as prev_amount,
		monthly_amount - LAG(monthly_amount) over (order by month) as mom_change
from monthly; 



