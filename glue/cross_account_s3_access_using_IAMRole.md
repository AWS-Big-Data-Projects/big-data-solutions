S3 bucket Example policy :


{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DelegateS3Access",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::destination-aws-account-id:role/destination-IAM-role-arn"
            },
            "Action": [
                "s3:Get*",
                "s3:List*",
                "s3:Put*"
            ],
            "Resource": [
                "arn:aws:s3:::source-s3-bucket/*",
                "arn:aws:s3:::source-s3-bucket"
            ]
        }
    ]
}


IAM Role Inline Policy Example :

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject*",
                "s3:GetBucketLocation",
                "s3:GetObjectTagging",
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:PutObjectTagging"
            ],
            "Resource": [
                "arn:aws:s3:::source-s3-bucket",
                "arn:aws:s3:::source-s3-bucket/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::destination-s3-bucket",
                "arn:aws:s3:::destination-s3-bucket/*"
            ]
        }
    ]
}
