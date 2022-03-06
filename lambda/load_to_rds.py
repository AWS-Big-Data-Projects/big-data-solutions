#
#Lambda function used to write inbound IoT sensor data to RDS PostgeSQL database
#
import sys
import os
import json
import psycopg2

#Connect to PostgreSQL database and insert sensor data record
def handler(event, context):

    try:
        conn = psycopg2.connect(host=os.environ['rds_host'], port=os.environ['rds_port'], 
                                dbname=os.environ['rds_dbname'], user=os.environ['rds_username'], 
                                password=os.environ['rds_password'])
        conn.autocommit = True
    
        cur = conn.cursor()
            
        cur.execute('insert into "SensorData" ("DeviceID", "DateTime", "Temperature", "Humidity", ' 
                    '"WindDirection", "WindIntensity", "RainHeight") values (%s, %s, %s, %s, %s, %s, %s)', 
                    (event['deviceid'], event['datetime'], event['temperature'], event['humidity'], 
                     event['windDirection'], event['windIntensity'], event['rainHeight']))
        cur.close()
        
    #No except statement is used since any exceptions should fail the function so that the
    #failed message is sent to the SQS destination configured for the Lambda function
    finally:
        try:
            conn.close()
        except:
            pass

#Used when testing from the Linux command line    
#if __name__== "__main__":
#    handler(None, None)
