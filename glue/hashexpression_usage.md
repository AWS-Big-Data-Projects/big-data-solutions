Issue Description : while trying to load the data is on to dynamic frame by reading from JDBC table in parallel using hashexpression, it left out the negative values present in the database.

Reason  : hashexpression only works on the positive integer values and left out the negative values present in the database.

Resolution : To resolve this issue, hashfield can be used in place of hashexpression. Also, As a workaround, we can use " ABS(columnname)" instead of "columnname" in hashexpression so that it can load negative value to the dynamic frame.

Method : Instead of using the method 1 we can use method 2 or method 3 to resolve the issue

METHOD 1:

additional_options = {"hashexpression": "idcase", 'hashpartitions': '10'} 

glueContext = GlueContext(sc)


df_data = glueContext.create_dynamic_frame_from_catalog(database=database, 

                                                                                                                          table_name=table_name, 

                                                                                                                          additional_options=additional_options)

df_data.toDF().show()

+------+-------+
|idcase|casecol|
+------+-------+
|     0|      e|
|     1|      f|
|     2|      g|
|     3|      h|
|     4|      i|
|     5|      j|
+------+-------+


METHOD 2: Using ABS(Columnname) in hashexpression

database = 'hello'
table_name = 'casedb_case'
additional_options = {"hashexpression": "ABS(idcase)", 'hashpartitions': '10'} 

glueContext = GlueContext(sc)
df_data = glueContext.create_dynamic_frame_from_catalog(database=database,
                                                        table_name=table_name, 
                                                        additional_options=additional_options)
df_data.toDF().show()

+------+-------+
|idcase|casecol|
+------+-------+
|     0|      e|
|    -1|      a|
|     1|      f|
|    -2|      b|
|     2|      g|
|    -3|      c|
|     3|      h|
|    -4|      d|
|     4|      i|
|     5|      j|

+------+-------+

METHOD 3: Using hashfield instead of hashexpression

database = 'hello'
table_name = 'casedb_case'
additional_options = {"hashfield": "idcase", 'hashpartitions': '10'} 

glueContext = GlueContext(sc)
df_data = glueContext.create_dynamic_frame_from_catalog(database=database,
                                                        table_name=table_name, 
                                                        additional_options=additional_options)
df_data.toDF().show()

+------+-------+
|idcase|casecol|
+------+-------+

|    -4|      d|

|    -3|      c|

|    -2|      b|

|    -1|      a|

|     0|      e|
|     1|      f|
|     2|      g|
|     3|      h|
|     4|      i|
|     5|      j|
+------+-------+
