KMS key policy to be used while setting up the glue crawler to use security config.

      {
             "Effect": "Allow",
             "Principal": { "Service": "logs.region.amazonaws.com",
             "AWS": [
                      "role1",
                      "role2",
                      "role3"
                   ] },
                          "Action": [
                                 "kms:Encrypt*",
                                 "kms:Decrypt*",
                                 "kms:ReEncrypt*",
                                 "kms:GenerateDataKey*",
                                 "kms:Describe*"
                          ],
                          "Resource": "*"
      }
