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
# BITOID            'bit'                           'bit'               +
# BOOLOID           'boolean'
# BPCHAROID         'character'                     'character'         +
# FLOAT4OID         'real'
# FLOAT8OID         'double precision'
# INT2OID           'smallint'
# INT4OID           'integer'
# INT8OID           'bigint'
# NUMERICOID        'numeric'                       'numeric'
# INTERVALOID       'interval'                      'interval'
# TIMEOID           'time without time zone'        'time'
# TIMETZOID         'time with time zone'           'time'
# TIMESTAMPOID      'timestamp without time zone'   'timestamp'
# TIMESTAMPTZOID    'timestamp with time zone'      'timestamp'
# VARBITOID         'bit varying'                   'bit varying'
# VARCHAROID        'character varying'             'character varying'

TYPES_SQL_TO_ODD = {

    'bit': 'TYPE_BINARY',  # BITOID recheck
    'boolean': 'TYPE_BOOLEAN',  # BOOLOID
    'character': 'TYPE_CHAR',  # BPCHAROID recheck

    'real': 'TYPE_NUMBER',  # FLOAT4OID
    'double precision': 'TYPE_NUMBER',  # FLOAT8OID
    'smallint': 'TYPE_INTEGER',  # INT2OID
    'integer': 'TYPE_INTEGER',  # INT4OID
    'bigint': 'TYPE_NUMBER',  # INT8OID recheck
    'numeric': 'TYPE_NUMBER',  # NUMERICOID

    'interval': 'TYPE_DURATION',  # INTERVALOID recheck
    'time': 'TYPE_DATETIME',  # TIMEOID, TIMETZOID
    'time without time zone': 'TYPE_DATETIME',  # TIMEOID
    'time with time zone': 'TYPE_DATETIME',  # TIMETZOID
    'timestamp': 'TYPE_DATETIME',  # TIMESTAMPOID, TIMESTAMPTZOID
    'timestamp without time zone': 'TYPE_DATETIME',  # TIMESTAMPOID
    'timestamp with time zone': 'TYPE_DATETIME',  # TIMESTAMPTZOID

    'bit varying': 'TYPE_BINARY',  # VARBITOID recheck
    'character varying': 'TYPE_STRING',  # VARCHAROID

    'ARRAY': 'TYPE_LIST',  # view information_schema.columns recheck
    'USER-DEFINED': 'TYPE_STRUCT'  # view information_schema.columns recheck

}

# views, base tables, external tables, and shared tables
# TABLE, VIEW, MATERIALIZED VIEW, or " " empty string that represents no information.
TABLE_TYPES_SQL_TO_ODD = {
    'BASE TABLE': 'DATASET_TABLE',
    'EXTERNAL TABLE': 'DATASET_TABLE',
    'SHARED TABLE': 'DATASET_TABLE',
    # 'VIEW': 'DATASET_VIEW',
    # 'MATERIALIZED VIEW': 'DATASET_VIEW',
    # 'EXTERNAL VIEW': 'DATASET_VIEW',
    # 'EXTERNAL MATERIALIZED VIEW': 'DATASET_VIEW',
    '': 'DATASET_UNKNOWN'

    # 'LOCAL TEMPORARY': 'DATASET_TABLE',
    # 'BASE TABLE': 'DATASET_TABLE',
    # 'EXTERNAL TABLE': 'DATASET_EXTERNAL_TABLE',
    # 'EXTERNAL VIEW': 'DATASET_EXTERNAL_VIEW',
    # 'EXTERNAL MATERIALIZED VIEW': 'DATASET_EXTERNAL_MATERIALIZED_VIEW',
    # 'SHARED TABLE': 'DATASET_SHARED_TABLE',
    # 'LOCAL TEMPORARY': 'DATASET_TEMPORARY_TABLE',
    # 'VIEW': 'DATASET_VIEW',
    # 'MATERIALIZED VIEW': 'DATASET_MATERIALIZED_VIEW',
    # '': 'DATASET_UNKNOWN'
}


# STORED PROCEDURE, EGULAR FUNCTION, AGGREGATED FUNCTION
FUNCTION_TYPES_SQL_TO_ODD = {
    'VIEW': 'DATATRANSFORMER_JOB',
    'MATERIALIZED VIEW': 'DATATRANSFORMER_JOB',
    'EXTERNAL VIEW': 'DATATRANSFORMER_JOB',
    'EXTERNAL MATERIALIZED VIEW': 'DATATRANSFORMER_JOB',
    # 'STORED PROCEDURE': 'DATATRANSFORMER_STORED_PROCEDURE',
    # 'REGULAR FUNCTION': 'DATATRANSFORMER_FUNCTION',
    # 'AGGREGATED FUNCTION': 'DATATRANSFORMER_AGGREGATED_FUNCTION',
    # 'STORED PROCEDURE': 'DATATRANSFORMER_JOB',
    # 'REGULAR FUNCTION': 'DATATRANSFORMER_JOB',
    # 'AGGREGATED FUNCTION': 'DATATRANSFORMER_JOB',
    '': 'DATATRANSFORMER_UNKNOWN'
}
