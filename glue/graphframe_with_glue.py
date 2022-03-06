import sys

from awsglue.transforms import *

from awsglue.utils import getResolvedOptions

from pyspark.context import SparkContext

from pyspark.sql import SQLContext

from awsglue.context import GlueContext

from awsglue.dynamicframe import DynamicFrame

from awsglue.job import Job

from pyspark.sql import SparkSession

from pyspark.sql.functions import udf

from pyspark.sql.types import StringType

from pyspark.sql import Row

from graphframes import *


glueContext = GlueContext(SparkContext.getOrCreate())

sc = SparkContext.getOrCreate()

sc.setCheckpointDir('/tmp/')


spark = glueContext.spark_session


v = spark.createDataFrame([
  ("a", "Alice", 34),
  ("b", "Bob", 36),
  ("c", "Charlie", 30),
], ["id", "name", "age"])
# Create an Edge DataFrame with "src" and "dst" columns
e = spark.createDataFrame([
  ("a", "b", "friend"),
  ("b", "c", "follow"),
  ("c", "b", "follow"),
], ["src", "dst", "relationship"])
# Create a GraphFrame
#from graphframes import *

g = GraphFrame(v, e)

# Query: Get in-degree of each vertex.
g.inDegrees.show()

# Query: Count the number of "follow" connections in the graph.
g.edges.filter("relationship = 'follow'").count()

# Run PageRank algorithm, and show results.
results = g.pageRank(resetProbability=0.01, maxIter=20)
results.vertices.select("id", "pagerank").show()

result = g.connectedComponents()
result.select("id", "component").orderBy("component").show()
