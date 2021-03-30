def generate_catalog_oddrn(data_source_oddr: str, catalog_name: str):
    return f'{data_source_oddr}/databases/{catalog_name}'


def generate_schema_oddrn(data_source_oddr: str, catalog_name: str, schema_name: str):
    return f'{data_source_oddr}/databases/{catalog_name}/schemas/{schema_name}'


def generate_table_oddrn(data_source_oddr: str, catalog_name: str, schema_name: str, table_name: str):
    return f'{data_source_oddr}/databases/{catalog_name}/schemas/{schema_name}/tables/{table_name}'


def generate_function_oddrn(data_source_oddr: str, catalog_name: str, schema_name: str, function_name: str):
    return f'{data_source_oddr}/databases/{catalog_name}/schemas/{schema_name}/functions/{function_name}'


def generate_call_oddrn(data_source_oddr: str, catalog_name: str, function_name: str):
    return f'{data_source_oddr}/databases/{catalog_name}/calls/{function_name}'
