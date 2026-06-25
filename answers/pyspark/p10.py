# p10 [window/hard]
# Implement solve(spark, transactions) -> DataFrame. Expected columns: month, monthly_amount, prev_amount, mom_change


def solve(spark: SparkSession, transactions: DataFrame) -> DataFrame:
    month_col = "month"
    monthly_amount_col = "monthly_amount"
    mom_change_col = "mom_change"
    prev_amount_col = "prev_amount"
    totalWindow = Window.orderBy(month_col)			
    
    return transactions.withColumn(month_col, col("txn_date").substr(1, 7)) \
                    .groupBy(month_col) \
                    .agg(F.sum("amount").alias(monthly_amount_col)) \
                    .withColumn(prev_amount_col, lag(monthly_amount_col).over(totalWindow)) \
                    .withColumn(mom_change_col, col(monthly_amount_col) - col(prev_amount_col)) \
                    .select(month_col, monthly_amount_col, prev_amount_col, mom_change_col)
