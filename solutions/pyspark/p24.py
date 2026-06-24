# p24 HAVING == filter AFTER aggregation. In Spark that's just .where() on the
# aggregated DataFrame (group filtering, not row filtering).
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark: SparkSession, employees: DataFrame) -> DataFrame:
    e = employees
    return (e.groupBy("dept")
            .agg(F.count(F.lit(1)).alias("headcount"),
                 F.avg("salary").alias("avg_salary"))
            .where((F.col("headcount") > 5) & (F.col("avg_salary") > 70000)))
