An "Unable to locate credentials" error indicates that Amazon S3 can't find the credentials to authenticate AWS API calls. To resolve this issue, make sure that your AWS credentials are correctly configured in the AWS CLI.

Note: If you still receive an error when running an AWS CLI command, make sure that you’re using the most recent AWS CLI version.

To check if the AWS CLI is configured with credentials, run this command:


$ aws configure list


Name                    Value                    Type            Location
----                    -----                    ----            --------
profile                <not set>                 None            None
access_key             ****************ABCD      config_file    ~/.aws/config
secret_key             ****************ABCD      config_file    ~/.aws/config
region                 us-west-2                 env            AWS_DEFAULT_REGION

If your credentials are configured using environment variables, then the command returns a response similar to the following:

Name                   Value                     Type            Location
----                   -----                     ----            --------
profile                <not set>                 None            None
access_key             ****************N36N      env    
secret_key             ****************cxxy      env    
region                 <not set>                 None            None

If your credentials are configured in an instance profile, the command returns a response similar to the following:

Name                    Value                    Type              Location
----                    -----                    ----              --------
profile                <not set>                 None               None
access_key             ****************YVEQ      iam-role
secret_key             ****************2a9N      iam-role
region                 <not set>                 None               None

If the command returns the following output, then no credentials are set:

Name                    Value             Type                Location
----                    -----             ----                --------
profile                <not set>          None                None
access_key             <not set>          None                None
secret_key             <not set>          None                None
region                 <not set>          None                None

Review the response to check whether credentials are missing or the stored credentials are incorrect. As necessary, update your credentials either by using the AWS CLI [1] , environment variables[2] or by attaching an instance profile to an EC2 instance.[3]

After you update your credentials, test running the application. 

Ref:

1. https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration
2. https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html#envvars-set
3. https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html
