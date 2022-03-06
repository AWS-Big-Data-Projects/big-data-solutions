Query exhausted errors can happen because of memory pressure on an Athena node, due to aggregation operator or join operators. It can happen because of multiple operators. In short, Presto uses a DAG in memory. When it runs out of memory for the DAG, it crashes because of its inability to use the disk as additional swap. 

You can see which operator is causing the issue by looking at the stack trace.

Athena uses Presto as a query engine. Presto runs different stages of a query in memory. For a small number of queries and for certain operators, Presto brings all the data into a single nodes memory and may fail because it cannot spill pages to disk when memory is exhausted. 

This is not a resource-related issue, but more related to how specific operators cannot handle large amounts of data. The Athena service team has rectified this for ‘GroupBy’ operator, enabling it to spill to disk now. We expect to finish the other operators in the coming months. 


    Re-organize the queries
    Convert data into Parquet/ORC formats and consider partitioning the data




Error : 

category: RESOURCE_ERROR
errorCode: EXCEEDED_MEMORY_LIMIT
msg: "EXCEEDED_LOCAL_MEMORY_LIMIT: Query exceeded per-node total memory limit of 14GB [Allocated: 18.49GB, Delta: 11.76MB, Top Consumers: {LazyOutputBuffer=10.72GB, HashBuilderOperator=6.64GB, PartitionedOutputOperator=1.49GB}]"


I can see that your query uses a total of n LEFT OUTER JOIN and a INNER JOIN collectively :

JOIN operations in general are extremely costly to run in terms of memory usage. JOINS can also be expensive depending on the potential amount of data involved in the JOIN. As such, using these operations with the size of the dataset that they are running on caused the Athena memory to fillup and your query to fail.

There are a number of potential optimizations that you could make on your query to potentially reduce its resource footprint in Athena. One of the immediate approach that I wanted you to test is using Partition projection[2]. Take a look at the documentation and proceed with the implementation .

Read link [1] below for a list of these optimizations and investigate applying them to your query.

For example, you could see if by changing the order of the GROUP BY columns based on their cardinality by the highest cardinality (that is, most number of unique values, distributed evenly) to the lowest, if it increases the performance or reduces the footprint of your query. This particular tip is #7 from link [1] below.

Try the Partition projection[2] at this point so that we can speed up query processing of highly partitioned tables and automate partition management.Also take a quick look at the optimizations mentioned in link [1] first before trying either.

----------
----------

Links:

[1] Performance tips for tuning Athena queries - https://aws.amazon.com/blogs/big-data/top-10-performance-tuning-tips-for-amazon-athena/

[2] https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html
