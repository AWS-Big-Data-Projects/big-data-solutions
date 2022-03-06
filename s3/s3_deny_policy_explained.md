{
    "Sid": "DenyPublicReadACL",
    "Effect": "Deny",
    "Principal": {
        "AWS": "*"
    },
    "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl"
    ],
    "Resource": "arn:aws:s3:::examplebucket/*",
    "Condition": {
        "StringEquals": {
            "s3:x-amz-acl": [
                "public-read",
                "public-read-write",
                "authenticated-read"
            ]
        }
    }
}



“Deny any Amazon S3 request to PutObject or PutObjectAcl in the bucket examplebucket when the request includes one of the following access control lists (ACLs): public-read, public-read-write, or authenticated-read.”

 Instead, IAM evaluates first if there is an explicit Deny. If there is not, IAM continues to evaluate if you have an explicit Allow and then you have an implicit Deny.
