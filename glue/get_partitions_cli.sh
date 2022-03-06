Example 1 : aws glue get-partitions --database-name mydb --table-name mytable --expression "category=1" --region us-west-2
Explanation : The way above CLI command will work is - it will fetch the partitions that match the above key criteria i.e.   "category=1" . 

Example 2 : aws glue get-partitions --database-name mydb --table-name mytable --expression category=1\ AND\ date=\'2018-08-30\' --region us-west-2
Explanation : In this another example - it demonstrates we are trying to fetch partitons information based on the expression which contains multiple partitions keys defined on the table present in the glue data catalog . 
