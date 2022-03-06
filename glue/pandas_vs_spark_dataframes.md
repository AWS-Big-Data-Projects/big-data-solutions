=========================================================
Diff. between Spark and Pandas DataFrame/ Pros & Cons
=========================================================

  4. Using Pandas vs Spark DataFrames ==>>  Since you are using CSV which is not supported natively by Spark, With Pandas, you easily read CSV files with read_csv() or write it using to_csv(). Spark and Pandas DataFrames are very similar. Still, Pandas API remains more convenient and powerful.The number of API calls made by using Pandas and Spark dataframe should not differ.But overall there are few differences I would like to call out while using one over the other as below : 

    A. Pandas and Spark DataFrame are designed for structural and semistructral data processing. Both share some similar properties (which I have discussed above). The few differences between Pandas and PySpark DataFrame are:

    B. Operation on Pyspark DataFrame run parallel on different nodes in cluster but, in case of pandas it is not possible.Pandas data frames are in-memory, single-server. So their size is limited by your server memory, and you will process them with the power of a single server.

    C. Operations in PySpark DataFrame are lazy in nature but, in case of pandas we get the result as soon as we apply any operation.

    D. In PySpark DataFrame, we can’t change the DataFrame due to it’s immutable property, we need to transform it. But in pandas it is not the case.
    
    E. Pandas API support more operations than PySpark DataFrame. Still pandas API is more powerful than Spark.
    
    F. Complex operations in pandas are easier to perform than Pyspark DataFrame
    
I found some more articles( Non-AWS docs ) for you to go through in order to get more details on pandas vs Spark DataFrames here . [1] , [2] and [3]

=================
RECOMMENDATION 
================

If your use case has a growing data where you probably have billions of rows and columns down the line ,involving complex operations like merging or grouping of data  it definitely require parallelization and distributed computing. These operations are very slow and quite expensive and become difficult to handle with a Pandas dataframe, which does not support parallelization. Hence I recommend Spark DataFrame over Pandas DataFrame.
