# Upload boto3 and awscli wheel file to your S3 bucket. Boto3 and awscli both of these wheel file are available in pypi.org. (https://pypi.org/project/)
#Insert below codes at the beginning of your python script. (The print statements can obviously be omitted)

import sys
    sys.path.insert(0, '/glue/lib/installation')
    keys = [k for k in sys.modules.keys() if 'boto' in k]
    for k in keys:
        if 'boto' in k:
           del sys.modules[k]
     
    import boto3
    print('boto3 version')
    print(boto3.__version__)
    
athena = boto3.client("athena")
res = athena.list_data_catalogs()
