=> How does table versioning work with AWS Glue ?

Basically, all of your Tables in the Data Catalog can have versions, which are different definitions of their schema and properties ordered in time. You can select the 'active' version of a table at any time. Every time you update the schema of a table, Glue creates a new version of your table and automatically updates the table's currently active version to the new one.

=> Is it the crawler that manages the tables versioning?

Not strictly. The crawler can update the schema of an existing table, which will result in a new version being created. But you can also create new versions manually.

=>  Is it possible to configure versioning? For example the number of versions we want to keep.

No, that's not an option at the moment. The only configuration that can be done is selecting the active version of a table.

=>  If we use AWS Glue ETL Jobs (https://docs.aws.amazon.com/glue/latest/dg/update-from-job.html) to update table schemas, will they be versioned?

Any operation that updates a table's schema will create a new version, including ETL jobs.
