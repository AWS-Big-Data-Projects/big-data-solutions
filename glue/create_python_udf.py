import pyspark
from pyspark import SQLContext
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, StringType
from pyspark.sql.functions import udf
from pyspark.sql import Row


conf = pyspark.SparkConf() 

 
sc = pyspark.SparkContext.getOrCreate(conf=conf)
spark = SQLContext(sc)

schema = StructType([
    StructField("sales", FloatType(),True),    
    StructField("employee", StringType(),True),
    StructField("ID", IntegerType(),True)
])

data = [[ 10.2, "Fred",123]]

df = spark.createDataFrame(data,schema=schema)

colsInt = udf(lambda z: toInt(z), IntegerType())
spark.udf.register("colsInt", colsInt)

def toInt(s):
    if isinstance(s, str) == True:
        st = [str(ord(i)) for i in s]
        return(int(''.join(st)))
    else:
         return Null


df2 = df.withColumn( 'semployee',colsInt('employee'))


#Ref: https://www.bmc.com/blogs/how-to-write-spark-udf-python/
