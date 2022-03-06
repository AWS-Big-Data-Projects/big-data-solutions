GetPartitionsResult result = glueClient.getPartitions(new GetPartitionsRequest()
                        .withCatalogId(CATALOG_ID)
                        .withDatabaseName(DATABASE_NAME)
                        .withTableName(TABLE_NAME)
                        .withExpression(expression));

List filteredPartitions = new ArrayList<>();

while(result.getNextToken()!=null){
	if (!result.getPartitions().isEmpty()) {
		filteredPartitions.addAll(result.getPartitions())
	}
	GetPartitionsResult result = glueClient.getPartitions(new GetPartitionsRequest()
                        .withCatalogId(CATALOG_ID)
                        .withDatabaseName(DATABASE_NAME)
                        .withTableName(TABLE_NAME)
                        .withExpression(expression)
                        .withNextToken(result.getNextToken()));
}

if (!result.getPartitions().isEmpty()) {
	filteredPartitions.addAll(result.getPartitions())
}

if (filteredPartitions.isEmpty()) {
	throw new HealthCheckException(
        String.format("Health Check Failed - 0 rows were generated for user case %s.", use_case));
}
