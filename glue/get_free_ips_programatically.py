import json
import sys
import json
import datetime
import csv
from botocore.exceptions import ClientError
def lambda_handler(event, context):

#########################################################################################
#Enter the inputs
#########################################################################################
    start_date = '2019-05-01'
    end_date = '2020-06-21'
    account_id = '731836818499'
    job_run_status = 'FAILED'
    bucket_name = 'testingdp'
#########################################################################################

    universal_list = []
    import boto3
    client = boto3.client('glue')
    client1 = boto3.client('cloudtrail')
    client2 = boto3.client('ec2')
    year, month, day = map(int, start_date.split('-'))
    year1, month1, day1 = map(int, end_date.split('-'))
    start = datetime.datetime(year, month, day)
    end = datetime.datetime(year1, month1, day1)

#########################################################################################
#Getting the Cloud-trail logs for getting the user who is running all those jobs
#########################################################################################
    t = client1.lookup_events(LookupAttributes=[{
            'AttributeKey': 'EventName',
            'AttributeValue': 'StartJobRun'},],
            StartTime=start,
            EndTime=end)

    dict = {}
    items1 = []

    while t:
        items1 = t['Events']
        for item in items1:

            json_file= json.loads(item['CloudTrailEvent'])
            if json_file['responseElements']!= None:
                g = json_file['responseElements']['jobRunId']
                w = item['Username']
                dict[g] = w
        t = client.lookup_events(LookupAttributes=[{
            'AttributeKey': 'EventName',
            'AttributeValue': 'StartJobRun'},],
            StartTime=start,
            EndTime=end,NextToken=t['NextToken']) if 'NextToken' in t else None

#########################################################################################
# Getting all the jobs and there job run ids and in this case we are getting all the job runs which are failed but we can change it to any status
#########################################################################################
    l = []
    getjobnames = client.get_jobs()
    joblist = []
    while getjobnames:
        items = getjobnames['Jobs']
        for item in items:
            joblist.append(item['Name'])
        getjobnames = client.get_jobs(NextToken=getjobnames['NextToken']) if 'NextToken' in getjobnames else None
    for i in joblist:
        connectionlist = []
        ActiveJobruns = {}
        Subnets_dict = {}

        clientjobrun = client.get_job_runs(JobName=i)
        while clientjobrun:
            items = clientjobrun['JobRuns']
            for item in items:

                if item['JobRunState'] == job_run_status:
                    ActiveJobruns[item['Id']] = item['StartedOn']

            clientjobrun = client.get_job_runs(JobName = i,NextToken=clientjobrun['NextToken']) if 'NextToken' in clientjobrun else None

#########################################################################################
#Getting all the jobs connections and their related free subnet ids
#########################################################################################
        jobdetails = client.get_job(JobName=i)
        e = jobdetails.get('Job')
        if e.get('Connections'):
            print(i)
            subnet_list = []
            connectionlist = jobdetails['Job']['Connections']['Connections']
            for connection in connectionlist:
                try:

                    subnetdetails = client.get_connection(CatalogId=account_id,Name=connection)
                    subnetid = subnetdetails['Connection']['PhysicalConnectionRequirements']['SubnetId']
                    subnet_list.append(subnetid)
                except ClientError as e:
                    if e.response['Error']['Code'] == 'EntityNotFoundException':
                        print(connection + " "+ "Connection Doesn't exist")
                    else:
                        print("Unexpected error: %s" % e)

            subnet_final = client2.describe_subnets(SubnetIds=subnet_list)

            Subnets = []

            while subnet_final:

                Subnets = subnet_final['Subnets']

                for y in Subnets:

                    Subnets_dict[y['SubnetId']] = y['AvailableIpAddressCount']

                subnet_final = client2.describe_subnets(SubnetIds=subnet_list, NextToken=subnet_final['NextToken']) if 'NextToken' in subnet_final else None
#########################################################################################
#Removing duplicates and then getting the final output
#########################################################################################
        set_A = set()
        set_B = set()
        for k in dict:
            set_A.add(k)
        for j in ActiveJobruns:
            set_B.add(j)
        set_c = set_A.intersection(set_B)

        for w in set_c:
            if dict[w]!=None:
                all = []
                all.append(ActiveJobruns[w])
                all.append(j)
                all.append(i)
                all.append(dict[k])
                all.append(Subnets_dict)

                universal_list.append(all)
#########################################################################################
# Writing the list of list as csv file format file
#########################################################################################
    file = open('/tmp/Export.csv', 'w+', newline ='')
    with file:
        write = csv.writer(file)
        write.writerows(universal_list)
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file('/tmp/Export.csv',bucket_name, 'Export.csv')
    return "Finish"
#########################################################################################
