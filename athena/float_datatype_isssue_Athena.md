
Since  Athena query engine is based on Presto. FLOAT datatype is not supported according to Presto documentation[1]. And also, according to the Athena documentation[2], FLOAT datatype can only be used in DDL statements.

Presto supports REAL and DOUBLE types for float-point values and you can use DOUBLE type to cast as you mentioned.

select (cast(8765435678 as REAL)/cast(87654 as REAL)) as result

References:
[1] https://prestodb.io/docs/current/language/types.html#floating-point
[2] https://docs.aws.amazon.com/athena/latest/ug/data-types.html
