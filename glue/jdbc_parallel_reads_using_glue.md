One can use this method for JDBC tables, that is, most tables whose base data is a JDBC data store. These properties are ignored when reading Amazon Redshift and Amazon S3 tables.

hashfield

    Set hashfield to the name of a column in the JDBC table to be used to divide the data into partitions. For best results, this column should have an even distribution of values to spread the data between partitions. This column can be of any data type. AWS Glue generates non-overlapping queries that run in parallel to read the data partitioned by this column. For example, if your data is evenly distributed by month, you can use the month column to read each month of data in parallel.


      'hashfield': 'month'
      

    AWS Glue creates a query to hash the field value to a partition number and runs the query for all partitions in parallel. To use your own query to partition a table read, provide a hashexpression instead of a hashfield.
hashexpression

    Set hashexpression to an SQL expression (conforming to the JDBC database engine grammar) that returns a whole number. A simple expression is the name of any numeric column in the table. AWS Glue generates SQL queries to read the JDBC data in parallel using the hashexpression in the WHERE clause to partition data.

    For example, use the numeric column customerID to read data partitioned by a customer number.


      'hashexpression': 'customerID'
      

    To have AWS Glue control the partitioning, provide a hashfield instead of a hashexpression.
hashpartitions

    Set hashpartitions to the number of parallel reads of the JDBC table. If this property is not set, the default value is 7.

    For example, set the number of parallel reads to 5 so that AWS Glue reads your data with five queries (or fewer).


  'hashpartitions': '5'
  
