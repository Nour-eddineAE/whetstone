# p23 [joins/med]
# Implement solve(spark, employees) -> DataFrame. Expected columns: emp_id1, emp_id2, dept


def solve(spark: SparkSession, employees: DataFrame) -> DataFrame:
    e1 = employees.alias("e1")
    e2 = employees.alias("e2")
    join_exp = (col("e1.emp_id") < col("e2.emp_id")) & (col("e1.dept") == col("e2.dept"))
    
    return e1 \
			.join(e2,  join_exp, how="inner") \
            .select(col("e1.emp_id"), col("e2.emp_id"), col("e1.dept")) \
            .distinct()