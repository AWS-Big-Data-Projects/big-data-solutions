If you would like to configure EMRFS consistent view with a configuration object during cluster launch, you can do so using the following configuration:
=================================================
[
    {
      "Classification": "emrfs-site",
      "Properties": {
        "fs.s3.maxRetries": "20",
        "fs.s3.consistent.retryPeriodSeconds": "10",
        "fs.s3.consistent": "true",
        "fs.s3.consistent.retryCount": "5",
        "fs.s3.consistent.metadata.tableName": "EmrFSMetadata"
      }
    }
]
=================================================
