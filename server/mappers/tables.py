from odd_contract.models import DataEntity

from mappers.columns import map_column
from oddrn import generate_table_oddrn, generate_owner_oddrn
from mappers.columns import ColumnsEnum
from odd_contract.models import DataSet


def map_table(aws_account: str, host_name: str, columns: list[tuple]) -> list[DataEntity]:
    data_entities: list[DataEntity] = []
    data_entity: DataEntity = DataEntity()
    table_catalog = ""
    table_schema = ""
    table_name = ""
    table_oddrn = ""

    for column in columns:

        if column[ColumnsEnum.database_name] != table_catalog or \
                column[ColumnsEnum.schema_name] != table_schema or \
                column[ColumnsEnum.table_name] != table_name:
            table_catalog = column[ColumnsEnum.database_name]
            table_schema = column[ColumnsEnum.schema_name]
            table_name = column[ColumnsEnum.table_name]

            table_oddrn = generate_table_oddrn(aws_account, host_name, table_catalog, table_schema, table_name)
            owner_oddrn = generate_owner_oddrn(aws_account, host_name, table_catalog, table_schema)

            data_entity = DataEntity()
            data_entities.append(data_entity)

            data_entity.oddrn = table_oddrn
            data_entity.name = table_name
            data_entity.owner = owner_oddrn
            data_entity.metadata = []
            data_entity.created_at = None
            data_entity.updated_at = None

            data_entity.dataset = DataSet()
            data_entity.dataset.parent_oddrn = None
            data_entity.dataset.description = None
            data_entity.dataset.rows_number = 0
            data_entity.dataset.subtype = "DATASET_TABLE"
            data_entity.dataset.field_list = []

        data_entity.dataset.field_list.extend(map_column(column, table_oddrn))

    return data_entities
