Option 1 : Using boto3 API "put_object_tagging" method .[1]

        Example :

            The following example adds tags to an existing object.

              response = client.put_object_tagging(
                  Bucket='examplebucket',
                  Key='HappyFace.jpg',
                  Tagging={
                      'TagSet': [
                          {
                              'Key': 'Key3',
                              'Value': 'Value3',
                          },
                          {
                              'Key': 'Key4',
                              'Value': 'Value4',
                          },
                      ],
                  },
              )

              print(response)
              Expected Output:

              {
                  'VersionId': 'null',
                  'ResponseMetadata': {
                      '...': '...',
                  },
              }
