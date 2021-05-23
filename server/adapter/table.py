from odd_contract.models import DataEntity, DataSet, DataTransformer
from adapter import MetadataTables, MetadataColumns, MetadataColumn, _data_set_metadata_schema_url_info, \
    _data_set_metadata_excluded_keys_info
from adapter.column import _map_column
from adapter.metadata import _append_metadata_extension
from adapter.type import TYPES_SQL_TO_ODD
from app.oddrn import generate_table_oddrn, generate_schema_oddrn


def _map_table(data_source_oddrn: str, mtables: MetadataTables, mcolumns: MetadataColumns) -> list[DataEntity]:
    data_entities: list[DataEntity] = []
    column_index: int = 0

    for mtable in mtables.items:

        table_catalog: str = mtable.database_name
        table_schema: str = mtable.schema_name
        table_name: str = mtable.table_name

        schema_oddrn: str = generate_schema_oddrn(data_source_oddrn, table_catalog, table_schema)
        table_oddrn: str = generate_table_oddrn(data_source_oddrn, table_catalog, table_schema, table_name)

        # DataEntity
        data_entity: DataEntity = DataEntity()
        data_entities.append(data_entity)

        data_entity.oddrn = table_oddrn
        data_entity.name = table_name
        data_entity.owner = mtable.all.table_owner

        if mtable.all.table_type == 'TABLE':  # data_entity.dataset.subtype == 'DATASET_TABLE'
            data_entity.metadata = []
            # it is for full tables only
            _append_metadata_extension(data_entity.metadata, _data_set_metadata_schema_url_info, mtable.info,
                                       _data_set_metadata_excluded_keys_info)

        if mtable.all.table_creation_time is not None:
            data_entity.updated_at = mtable.all.table_creation_time.isoformat()
            data_entity.created_at = mtable.all.table_creation_time.isoformat()

        if mtable.base is not None:
            data_entity.description = mtable.base.remarks

        data_entity.type = TYPES_SQL_TO_ODD[mtable.base.table_type] \
            if mtable.base.table_type in TYPES_SQL_TO_ODD else 'UNKNOWN' 

        # Dataset
        data_entity.dataset = DataSet()

        data_entity.dataset.parent_oddrn = schema_oddrn

        if mtable.info is not None:
            if mtable.info.estimated_visible_rows is not None:
                data_entity.dataset.rows_number = int(mtable.info.estimated_visible_rows)
            else:
                if mtable.info.tbl_rows is not None:
                    data_entity.dataset.rows_number = int(mtable.info.tbl_rows)

        data_entity.dataset.field_list = []

        # DataTransformer
        if mtable.all.table_type == 'VIEW':
            data_entity.data_transformer = DataTransformer()

            # data_entity.data_transformer.source_code_url = None
            data_entity.data_transformer.sql = mtable.all.view_ddl

            data_entity.data_transformer.inputs = []
            data_entity.data_transformer.outputs = []

        # DatasetField
        while column_index < len(mcolumns.items):  # exclude right only rows
            mcolumn: MetadataColumn = mcolumns.items[column_index]

            if mcolumn.database_name == table_catalog and \
                    mcolumn.schema_name == table_schema and \
                    mcolumn.table_name == table_name:
                data_entity.dataset.field_list.extend(_map_column(mcolumn, data_entity.owner, table_oddrn))
                column_index += 1
            else:
                break

    return data_entities
