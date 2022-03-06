created a postgreSQL table: 

create table test(id numeric, name varchar);

insert into test (id,name) values(1.20,'abc') ;

#######

df = spark.read.format("jdbc").option("url","jdbc:postgresql://postgresssql.chj4saov4rkl.us-east-1.rds.amazonaws.com:5432/postgres").option("user", "postgres").option("password", "xxx,123").option("dbTable", "test").option("fetchSize", "50000").option("driver", "org.postgresql.Driver").load()

print("count")
print(df.count())
print(df.printSchema())
