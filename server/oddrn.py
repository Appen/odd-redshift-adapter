def generate_catalog_oddrn(aws_account: str, host_name: str):
    return f"//aws/{aws_account}/redshift/{host_name}"


def generate_owner_oddrn(aws_account: str, host_name: str, catalog_name: str, owner_name: str):
    return f"//aws/{aws_account}/redshift/{host_name}/databases/{catalog_name}/owners/{owner_name}"


def generate_table_oddrn(aws_account: str, host_name: str, catalog_name: str, schema_name: str, table_name: str):
    return f"//aws/{aws_account}/redshift/{host_name}" \
           f"/databases/{catalog_name}/schemas/{schema_name}/tables/{table_name}"
