# p02 left join: keep every employee; dept_id is NULL when no match.
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def solve(spark, dfs):
    e, d = dfs["employees"], dfs["departments"]
    return (e.join(d, e.dept == d.dept_name, "left")
            .select(e.emp_id, e.name, d.dept_id))
