Using AWS CLI command. [2]

      Example:

          The following put-object-tagging example sets a tag with the key designation and the value confidential on the specified object.

                aws s3api put-object-tagging \
                    --bucket my-bucket \
                    --key doc1.rtf \
                    --tagging '{"TagSet": [{ "Key": "designation", "Value": "confidential" }]}'
