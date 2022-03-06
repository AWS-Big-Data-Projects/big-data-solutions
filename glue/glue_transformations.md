    Relationalize converts a nested dataset stored in a DynamicFrameto a relational (rows and columns) format. Nested structures are unnested into top level columns and arrays decomposed into different tables with appropriate primary and foreign keys inserted. The result is a collection of DynamicFrames representing a set of tables that can be directly inserted into a relational database. More detail about relationalize can be found here.

    ## An example relationalizing and writing to Redshift
    dfc = history.relationalize("hist_root", redshift_temp_dir)
    ## Cycle through results and write to Redshift.
    for df_name in dfc.keys():
        df = dfc.select(df_name)
        print "Writing to Redshift table: ", df_name, " ..."
        glueContext.write_dynamic_frame.from_jdbc_conf(frame = df, 
            catalog_connection = "redshift3", 
            connection_options = {"dbtable": df_name, "database": "testdb"}, 
            redshift_tmp_dir = redshift_temp_dir)

    Unbox parses a string field of a certain type, such as JSON, into individual fields with their corresponding data types and store the result in a DynamicFrame. For example, you may have a CSV file with one field that is in JSON format {“a”: 3, “b”: “foo”, “c”: 1.2}. Unbox will reformat the JSON string into three distinct fields: an int, a string, and a double. The Unbox transformation is commonly used to replace costly Python User Defined Functions required to reformat data that may result in Apache Spark out of memory exceptions. The following example shows how to use Unbox:

    df_result = df_json.unbox('json', "json")

    ResolveChoice: AWS Glue Dynamic Frames support data where a column can have fields with different types. These columns are represented with Dynamic Frame’s choice type. For example, Dynamic Frame schema for the medicare dataset shows up as follows:

    root
     |-- drg definition: string
     |-- provider id: choice
     |    |-- long
     |    |-- string
     |-- provider name: string
     |-- provider street address: string

    This is because the “provider id” column could either be a long or string type. The Apache Spark Dataframe considers the whole dataset and is forced to cast it to the most general type, namely string. Dynamic Frames allow you to cast the type using the ResolveChoice transform. For example, you can cast the column to long type as follows.

    medicare_res = medicare_dynamicframe.resolveChoice(specs = [('provider id','cast:long')])

    medicare_res.printSchema()
     
    root
     |-- drg definition: string
     |-- provider id: long
     |-- provider name: string
     |-- provider street address: string

    This transform would also insert a null where the value was a string that could not be cast. As a result, the records with string type casted to null values can also be identified now. Alternatively, the choice type can also be cast to struct, which keeps values of both types.

