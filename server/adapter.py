import psycopg2
from odd_contract.models import DataEntity

from mappers.tables import map_table


def _get_records(sql_query: str) -> list[tuple]:
    # use environment variables for connect
    connection = psycopg2.connect("postgresql://")
    cursor = connection.cursor()
    cursor.execute(sql_query)
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    return records


class RedshiftAdapter:
    __aws_account: str = "123456789012"

    def __init__(self, host_name: str) -> None:
        self.__host_name: str = host_name

    def get_aws_account(self) -> str:
        if self.__aws_account is None or self.__aws_account == "123456789012":
            records = _get_records("select current_aws_account")
            if len(records) == 1:
                self.__aws_account = records[0][0]
        return self.__aws_account

    def get_datasets(self) -> list[DataEntity]:
        records = _get_records(
            "select database_name, schema_name, table_name, column_name, column_default, is_nullable, data_type "
            "from SVV_ALL_COLUMNS "
            "order by database_name, schema_name, table_name, ordinal_position")
        return map_table(self.get_aws_account(), self.__host_name, records)
