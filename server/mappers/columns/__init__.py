from enum import IntEnum, unique
from odd_contract.models import DataSetField, DataSetFieldType


@unique
class ColumnsEnum(IntEnum):
    database_name = 0
    schema_name = 1
    table_name = 2
    column_name = 3
    column_default = 4
    is_nullable = 5
    data_type = 6


# https://www.postgresql.org/docs/current/datatype.html
# The following types (or spellings thereof) are specified by SQL:
# bigint, bit, bit varying, boolean, char, character varying, character, varchar,
# date, double precision, integer, interval, numeric, decimal, real, smallint,
# time (with or without time zone), timestamp (with or without time zone), xml.
#
# See for development:
# view information_schema.columns, routine pg_catalog.format_type
# source https://github.com postgres/postgres src/backend/utils/adt/format_type.c
# https://github.com/postgres/postgres/blob/ca3b37487be333a1d241dab1bbdd17a211a88f43/src/backend/utils/adt/format_type.c
#
# Constant          Non Typmod                      Typmod              Exception
# BITOID            "bit"                           "bit"               +
# BOOLOID           "boolean"
# BPCHAROID         "character"                     "character"         +
# FLOAT4OID         "real"
# FLOAT8OID         "double precision"
# INT2OID           "smallint"
# INT4OID           "integer"
# INT8OID           "bigint"
# NUMERICOID        "numeric"                       "numeric"
# INTERVALOID       "interval"                      "interval"
# TIMEOID           "time without time zone"        "time"
# TIMETZOID         "time with time zone"           "time"
# TIMESTAMPOID      "timestamp without time zone"   "timestamp"
# TIMESTAMPTZOID    "timestamp with time zone"      "timestamp"
# VARBITOID         "bit varying"                   "bit varying"
# VARCHAROID        "character varying"             "character varying"

TYPES_SQL_TO_ODD = {

    "bit": "TYPE_BINARY",  # BITOID recheck
    "boolean": "TYPE_BOOLEAN",  # BOOLOID
    "character": "TYPE_CHAR",  # BPCHAROID recheck

    "real": "TYPE_NUMBER",  # FLOAT4OID
    "double precision": "TYPE_NUMBER",  # FLOAT8OID
    "smallint": "TYPE_INTEGER",  # INT2OID
    "integer": "TYPE_INTEGER",  # INT4OID
    "bigint": "TYPE_NUMBER",  # INT8OID recheck
    "numeric": "TYPE_NUMBER",  # NUMERICOID

    "interval": "TYPE_DURATION",  # INTERVALOID recheck
    "time": "TYPE_DATETIME",  # TIMEOID, TIMETZOID
    "time without time zone": "TYPE_DATETIME",  # TIMEOID
    "time with time zone": "TYPE_DATETIME",  # TIMETZOID
    "timestamp": "TYPE_DATETIME",  # TIMESTAMPOID, TIMESTAMPTZOID
    "timestamp without time zone": "TYPE_DATETIME",  # TIMESTAMPOID
    "timestamp with time zone": "TYPE_DATETIME",  # TIMESTAMPTZOID

    "bit varying": "TYPE_BINARY",  # VARBITOID recheck
    "character varying": "TYPE_STRING",  # VARCHAROID

    "ARRAY": "TYPE_LIST",  # view information_schema.columns recheck
    "USER-DEFINED": "TYPE_STRUCT"  # view information_schema.columns recheck

}


def map_column(column: tuple,
               table_oddrn: str,
               parent_oddrn: str = None,
               is_key: bool = None,
               is_value: bool = None
               ) -> list[DataSetField]:
    result: list[DataSetField] = []
    name = column[ColumnsEnum.column_name]
    resource_name = "keys" if is_key else "values" if is_value else "subcolumns"

    dsf = DataSetField()
    dsf.name = name
    dsf.oddrn = f'{table_oddrn}/columns/{name}' if parent_oddrn is None else f'{parent_oddrn}/{resource_name}/{name}'
    dsf.parent_field_oddrn = parent_oddrn
    dsf.type = DataSetFieldType()
    if column[ColumnsEnum.data_type] in TYPES_SQL_TO_ODD:
        dsf.type.type = TYPES_SQL_TO_ODD[column[ColumnsEnum.data_type]]
    else:
        dsf.type.type = 'TYPE_STRING'
    dsf.type.logical_type = column[ColumnsEnum.data_type]
    dsf.type.is_nullable = True if column[ColumnsEnum.is_nullable] == 'YES' else False
    dsf.is_key = bool(is_key)
    dsf.is_value = bool(is_value)
    dsf.default_value = column[ColumnsEnum.column_default]

    result.append(dsf)
    return result
