import datetime
from pyspark.sql.types import Row, StructType, StructField, StringType, IntegerType, DateType
from pyspark.sql.functions import col, to_date

schema = StructType([
  StructField('A', IntegerType(), True),
  StructField('date', DateType(), True)
])

values=sc.parallelize([(3,'2012-02-02'),(5,'2018-08-08')])

rdd= values.map(lambda t: Row(A=t[0],date=datetime.datetime.strptime(t[1], "%Y-%m-%d")))

df = sqlContext.createDataFrame(rdd, schema)

from pyspark.sql.functions import lit


df5 = df4.withColumn("name", lit('ishan'))

df6 = df5.withColumn("roll_id", lit(7))
