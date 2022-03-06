import boto3
import sys
import pymysql
from awsglue.utils import getResolvedOptions


args = getResolvedOptions(sys.argv,['env'])

client = boto3.client('ssm', region_name='us-east-1')
text = '/ishan/'+args['env']+'/mysql/'
response = client.get_parameters(Names=[text+'bucketname',text+'dbuser',text+'dbpassword', text+'host', text+'dbname', text+'dbport' ],WithDecryption=False)

dict = {}
parameters = response['Parameters']
for i in parameters:
    name = i['Name']
    value = i['Value']
    dict[name]  = value
    
Bucket = dict[text+'bucketname']
hostName = dict[text+'host']
portNum = dict[text+'dbport']
usr = dict[text+'dbuser']
pswrd = dict[text+'dbpassword']
dbName = dict[text+'dbname']


def execSql(key):
    s3 = boto3.resource('s3')
    
    query=s3.Object(Bucket, key).get()['Body'].read().decode('utf-8')
    # conn = mysql.connector.connect(
conn = pymysql.connect(host= hostName,port=portNum,user=usr,password=pswrd,database= dbName)
conn = pymysql.connect(host="<database-url", port=3306, user="<user-name>", password="<password>", database="<database-name>")
    
    #conn.raise_on_warnings = True
    try:
        # cur = conn.cursor(buffered=True)
        cur = conn.cursor()
        cur = conn.cursor()
        cur.execute
        sqlCommands = query.split(';')
        print(query)
        for command in sqlCommands:
            print(command)
            if (command != ''):
                print('SQL Query to be executed:' + command)
                cur.execute(command)
    except Error as e:
        raise Exception("{}:Exception raised: {}".format(e))
    finally:
        cur.close()
        conn.close() 
     

key_1 = 'SQL/test.sql'

print("running script 1")
execSql(key_1)

print("All scripts completed successfully")
