--------------
current_timestamp as insert_timestamp,
current_timestamp as update_timestamp,
current_timestamp as created_at
--------------

And since this field is of type "timestamp with time zone", it creates an issue because Athena doesn't support column definition of this type. 

As an example:

SELECT current_timestamp

Example Result: 2020-03-11 11:02:14.633 UTC

SELECT typeof(current_timestamp)

Result: timestamp with time zone

Now, if we try to create a table out of this SELECT statement:

CREATE TABLE test AS SELECT current_timestamp as time

Result: NOT_SUPPORTED: Unsupported Hive type: timestamp with time zone.

So, to address this, we could cast this data type into one of the support types, such as:

CREATE TABLE test AS SELECT cast(current_timestamp as timestamp) as time
Result: Query successful. 
