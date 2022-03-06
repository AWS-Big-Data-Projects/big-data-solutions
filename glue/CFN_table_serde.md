CloudFormation of Glue Table that particularly has a SerDe parameters and Table properties.

SalesPipelineTable:
    Type: "AWS::Glue::Table"
    DependsOn: MarketingAndSalesDatabase
    Properties:
      TableInput:
        Description: "Sales Pipeline table (Amazon QuickSight Sample)."
        TableType: "EXTERNAL_TABLE"
        Parameters: {
                "CrawlerSchemaDeserializerVersion": "1.0",
                "compressionType": "none",
                "classification": "csv",
                "recordCount": "16831",
                "typeOfData": "file",
                "CrawlerSchemaSerializerVersion": "1.0",
                "columnsOrdered": "true",
                "objectCount": "1",
                "delimiter": ",",
                "skip.header.line.count": "1",
                "averageRecordSize": "119",
                "sizeKey": "2002910"
        }
        StorageDescriptor:
          StoredAsSubDirectories: False
          Parameters: {
                  "CrawlerSchemaDeserializerVersion": "1.0",
                  "compressionType": "none",
                  "classification": "csv",
                  "recordCount": "16831",
                  "typeOfData": "file",
                  "CrawlerSchemaSerializerVersion": "1.0",
                  "columnsOrdered": "true",
                  "objectCount": "1",
                  "delimiter": ",",
                  "skip.header.line.count": "1",
                  "averageRecordSize": "119",
                  "sizeKey": "2002910"
          }
          InputFormat: "org.apache.hadoop.mapred.TextInputFormat"
          OutputFormat: "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"
          Columns:
            - Type: string
              Name: date
            - Type: string
              Name: salesperson
            - Type: string
              Name: lead name
            - Type: string
              Name: segment
            - Type: string
              Name: region
            - Type: string
              Name: target close
            - Type: bigint
              Name: forecasted monthly revenue
            - Type: string
              Name: opportunity stage
            - Type: bigint
              Name: weighted revenue
            - Type: boolean
              Name: closed opportunity
            - Type: boolean
              Name: active opportunity
            - Type: boolean
              Name: latest status entry
          SerdeInfo:
            Parameters: {
                        "field.delim": ","
            }
            SerializationLibrary: "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe"
          Compressed: False
          Location: !Sub "s3://${DataBucketName}/sales/"
        Retention: 0
        Name: !Ref SalesPipelineTableName
      DatabaseName: !Ref MarketingAndSalesDatabaseName
      CatalogId: !Ref AWS::AccountId
      
      Ref: 
      
      
[1] https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html
[2] https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html
[3] https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html
[4] https://github.com/aws-samples/aws-etl-orchestrator
[5] https://github.com/aws-samples/aws-etl-orchestrator/blob/master/cloudformation/glue-resources.yaml
