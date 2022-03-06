As of today Glue dynamic-frame does not support adding new column fields directly, like we are able to do in case of Spark data-frames using "withColumn()"

#Approach 1 : Converting a Glue Dynamic-frame to a Spark Data-frame, using withColumns() to add a column and then converting it back to a Glue Dynamic-frame.
 
Here is the code snippet that I used -
====================
start1 = time.time()
spark_df = my_dynamic_frame.toDF()
break1 = time.time()
spark_df= spark_df.withColumn('some_date', lit(datetime.now()))
break2 = time.time()
glue_df= DynamicFrame.fromDF(spark_df, glueContext, "glue_df1")
end1 = time.time()
print("Time taken for Approach 1 - " + str(end1-start1))
print("Time taken to add column in traditional spark df using withColumn() - " + str(break2-break1))
====================
 
Observations -
Time taken for  Approach 1 - 3.7365798950195312
Time taken to add column in traditional spark df using withColumn() - 0.5842971801757812
 
Here we can also observe that a good amount of the execution time was spent in performing the toDF() and fromDF() actions and they are operationally expensive.
 
#Approach 2 : Using Map class[2] and building a new DynamicFrame by applying a function to all the records in the input DynamicFrame which will add the new column.
 
Here is the code snippet that I used -
=====================
def AddProcessedTime(r):
    r["jobProcessedDateTime"] = datetime.today() 
    return r
 
start2 = time.time() 
mapped_dyF = Map.apply(frame = my_dynamic_frame, f = AddProcessedTime)
end2= time.time()
print("Time taken for Approach 2 - " + str(end2-start2))
=====================
 
Observations -
Time taken for Approach 2 - 0.06092071533203125
 
#Approach 3 : Ingest this data from S3 in the form of a native PySpark DataFrame directly.
Note: Here I am using the sample file over which the Glue data catalog table in Approach 1 and 2 was made.
 
Here is the code snippet that I used -
=========================
start3 = time.time() 
spark_df1= spark.read.csv("s3://<my-bucket>/<my-folder>/sample.csv")
end3= time.time()
print("Time taken for Approach 3 - " + str(end3-start3))
=========================
 
Observations -
Time taken for Approach 3 - 4.811927795410156

 
Test Analysis -
+++++++++++++++++++++++
1. Time taken to add column in traditional spark df using withColumn() = 0.5842971801757812
2. Time taken for Approach 1 = 3.7365798950195312
3. Time taken for  Approach 2 = 0.06092071533203125  ( fastest )
4. Time taken for  Approach 3 = 4.811927795410156
++++++++++++++++++++++++
 
Hence, on the basis of the above test, we can observe that the Approach 2 seems to be faster in terms of execution time than the other approaches which we tested and can be used for adding the columns in your Glue Dynamic-frame as a suitable work-around. 
 
