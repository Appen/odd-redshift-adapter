from odd_contract.models import DataSetField, DataSetFieldType, DataSetFieldStat
from adapter import MetadataColumn, _data_set_field_metadata_schema_url, \
    _data_set_field_metadata_schema_url_redshift, _data_set_field_metadata_schema_url_external
from adapter.type import TYPES_SQL_TO_ODD
from adapter.metadata import _append_metadata_extension


def _map_column(mcolumn: MetadataColumn,
                schema_oddrn: str, table_oddrn: str, parent_oddrn: str = None,
                is_key: bool = None, is_value: bool = None
                ) -> list[DataSetField]:
    result: list[DataSetField] = []

    name: str = mcolumn.base.column_name
    resource_name: str = 'keys' if is_key else 'values' if is_value else 'subcolumns'

    dsf: DataSetField = DataSetField()

    dsf.oddrn = f'{table_oddrn}/columns/{name}' if parent_oddrn is None else f'{parent_oddrn}/{resource_name}/{name}'
    dsf.name = name
    dsf.owner = schema_oddrn

    dsf.metadata = []
    _append_metadata_extension(dsf.metadata, _data_set_field_metadata_schema_url, mcolumn.base)
    _append_metadata_extension(dsf.metadata, _data_set_field_metadata_schema_url_redshift, mcolumn.redshift)
    _append_metadata_extension(dsf.metadata, _data_set_field_metadata_schema_url_external, mcolumn.external)

    dsf.parent_field_oddrn = parent_oddrn

    dsf.type = DataSetFieldType()
    data_type: str = mcolumn.base.data_type
    dsf.type.type = TYPES_SQL_TO_ODD[data_type] if data_type in TYPES_SQL_TO_ODD else 'TYPE_STRING'  # TYPE_UNKNOWN
    dsf.type.logical_type = mcolumn.base.data_type
    dsf.type.is_nullable = True if mcolumn.base.is_nullable == 'YES' else False

    dsf.is_key = bool(is_key)
    dsf.is_value = bool(is_value)
    dsf.default_value = mcolumn.base.column_default
    dsf.description = mcolumn.base.remarks

    dsf.stats = DataSetFieldStat()
    # DataSetFieldStat

    result.append(dsf)
    return result