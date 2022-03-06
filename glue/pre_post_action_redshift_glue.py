import boto3
import json
import logging
import sys

from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

from utils import updateColumnList, createExternalTableDf, createFinalDynamicFrame, createRedshiftTableDF, \
    settingContextVariable, retrieveGlueArguments

logging.getLogger().setLevel(logging.INFO)


def getSecretPassword(user, database):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name='us-east-1')
    try:
        get_secret_value_response = client.get_secret_value(SecretId=user)
        if 'SecretString' in get_secret_value_response:
            text_secret_data = get_secret_value_response['SecretString']
        else:
            text_secret_data = get_secret_value_response['SecretBinary']
        logging.info("Secrets Manager Credentials for Redshift")
        secret = json.loads(text_secret_data)
        username = secret.get('username')
        password = secret.get('password')
        host = secret.get('host')
        port = secret.get('port')
        url = "jdbc:redshift://" + host + ":" + str(port) + "/" + database
    except Exception as e:
        logging.error("Script failed with error " + str(e))
        sys.exit(str(e))
    return username, password, url


def queryCreation(final_table, staging_table, joining_condition):
    pre_query = """delete from %s using %s where %s""" % (final_table, staging_table, joining_condition)
    logging.info(pre_query)
    post_query = """ truncate table %s """ % staging_table
    logging.info(post_query)
    return pre_query, post_query


try:
    args = getResolvedOptions(sys.argv, ['TempDir', 'dbTable', 'dbTableStagingName', 'dbTablePrimaryKeys',
                                         'dbStagingTablePrimaryKeys', 'hashTableFilter', 'hashMapTableName',
                                         'hashDatabase', 'jdbcDatabase', 'db_aws_iam_role', 'secretName',
                                         'customerColumnNames', 'customerHashMap', 'stagingMapTableJoinKey'])
    variable_list = ['TempDir', 'dbTable', 'dbTableStagingName', 'dbTablePrimaryKeys', 'dbStagingTablePrimaryKeys',
                     'hashTableFilter',
                     'hashMapTableName', 'hashDatabase', 'jdbcDatabase',
                     'db_aws_iam_role', 'secretName', 'customerColumnNames', 'customerHashMap',
                     'stagingMapTableJoinKey']

    logging.info("Setting up the argument values")
    temp_dir, db_table, db_table_staging_name, db_table_primary_key, db_staging_table_primary_key, hash_table_filter, \
    hash_map_table_name, hash_database, jdbc_database, db_aws_iam_role, secret_name, customerColumnName, \
    customer_hash_map, staging_map_table_join_key = retrieveGlueArguments(args, variable_list)

    db_table_primary_keys = db_table_primary_key.split(',')
    customerColumnNames = customerColumnName.split(',')
    db_staging_table_primary_keys = db_staging_table_primary_key.split(',')
    join_condition = ' AND '.join(
        ['cast(%s.%s as varchar(255)) = cast(%s.%s as varchar(255))' % (
            db_table, final_table_key, db_table_staging_name, staging_table_key) for
         final_table_key, staging_table_key in zip(db_table_primary_keys, db_staging_table_primary_keys)])

    logging.info("Retrieving Redshift credentials")
    redshift_user = 'xx/Redshift/' + secret_name
    db_username, db_password, db_url = getSecretPassword(redshift_user, jdbc_database)

    logging.info("Setting up context variables")
    GLUE_CONTEXT, SPARK, REDSHIFT_UPSERT_JOB = settingContextVariable(SparkContext, GlueContext, Job)

    logging.info("creating Data Frame on Staging Table")
    staging_source_df = createRedshiftTableDF(db_url, db_table_staging_name, db_username, db_password, temp_dir,
                                              db_aws_iam_role, GLUE_CONTEXT)

    logging.info("creating final table column list")
    columns_to_query_str = updateColumnList(customerColumnNames, staging_source_df.columns, customer_hash_map)

    logging.info("Creating data frame on customer hash table")
    hash_map_table_df = createExternalTableDf(hash_database, hash_map_table_name, temp_dir, db_aws_iam_role,
                                              GLUE_CONTEXT,
                                              hash_table_filter)

    logging.info("Creating final dynamic frame")
    df_final = createFinalDynamicFrame(hash_map_table_df, staging_source_df, columns_to_query_str, SPARK, GLUE_CONTEXT,
                                       logging, DynamicFrame, staging_map_table_join_key)

    logging.info("Creating pre and post action query on the table")
    preQuery, postQuery = queryCreation(db_table, db_table_staging_name, join_condition)

    connection_options_load = {
        "preactions": preQuery,
        "postactions": postQuery,
        "dbtable": db_table,
        "database": jdbc_database,
        "user": db_username,
        "password": db_password,
        "aws_iam_role": db_aws_iam_role
    }

    logging.info('Triggering Data load to Redshift')
    datasink = GLUE_CONTEXT.write_dynamic_frame.from_jdbc_conf(
        frame=df_final,
        catalog_connection=jdbc_database,
        connection_options=connection_options_load,
        redshift_tmp_dir=temp_dir,
        transformation_ctx="datasink")

    REDSHIFT_UPSERT_JOB.commit()
except Exception as e:
    logging.error("Glue Job Failed: " + str(e))
    sys.exit(str(e))

