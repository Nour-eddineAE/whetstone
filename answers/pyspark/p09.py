# p09 [window/med]
# Implement solve(spark, transactions) -> DataFrame. Expected columns: user_id, txn_id, txn_date, amount, running_total


def solve(spark: SparkSession, transactions: DataFrame) -> DataFrame:
	
    totalWindow = Window.partitionBy("user_id") \
    					.orderBy(col("txn_date"), col("txn_id")) \
    					.rowsBetween(Window.unboundedPreceding, Window.currentRow)
    
    return transactions.withColumn("running_total", F.sum("amount").over(totalWindow)) \
                		.select("user_id", "txn_id", "txn_date", "amount", "running_total")


			