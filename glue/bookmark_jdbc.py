datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "new_stats", table_name = "statsdb_daily_device_usage", transformation_ctx = "datasource0",additional_options = {"hashfield":"start_time","jobBookmarkKeys":["start_time"],"jobBookmarksKeysSortOrder":"asc"})
+++++++++++
