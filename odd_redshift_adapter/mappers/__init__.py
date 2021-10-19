from collections import namedtuple

_METADATA_SCHEMA_URL_PREFIX: str = \
    'https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/' \
    'extensions/redshift.json#/definitions/Redshift'

_data_set_metadata_schema_url: str = _METADATA_SCHEMA_URL_PREFIX + 'DataSetExtensionBase'
_data_set_metadata_schema_url_all: str = _METADATA_SCHEMA_URL_PREFIX + 'DataSetExtensionAll'
_data_set_metadata_schema_url_redshift: str = _METADATA_SCHEMA_URL_PREFIX + 'DataSetExtensionRedshift'
_data_set_metadata_schema_url_external: str = _METADATA_SCHEMA_URL_PREFIX + 'DataSetExtensionExternal'
_data_set_metadata_schema_url_info: str = _METADATA_SCHEMA_URL_PREFIX + 'DataSetExtension'

_data_set_field_metadata_schema_url: str = _METADATA_SCHEMA_URL_PREFIX + 'DataSetFieldExtensionBase'
_data_set_field_metadata_schema_url_redshift: str = _METADATA_SCHEMA_URL_PREFIX + 'DataSetFieldExtension'
_data_set_field_metadata_schema_url_external: str = _METADATA_SCHEMA_URL_PREFIX + 'DataSetFieldExtensionExternal'

_data_set_metadata_schema_url_function: str = _METADATA_SCHEMA_URL_PREFIX + 'DataSetExtensionFunction'
_data_set_metadata_schema_url_call: str = _METADATA_SCHEMA_URL_PREFIX + 'DataSetExtensionCall'

_data_set_metadata_excluded_keys_info: set = {'database', 'schema', 'table'}

_data_set_field_metadata_excluded_keys_redshift: set = {'database_name', 'schema_name', 'table_name', 'column_name',
                                                    'data_type', 'column_default', 'is_nullable', 'remarks'}

_table_metadata: str = 'table_catalog, table_schema, table_name, table_type, remarks'
_table_table: str = 'pg_catalog.svv_tables ' \
                    'where table_schema not in (\'pg_toast\', \'pg_internal\', \'catalog_history\', ' \
                    '\'pg_catalog\', \'information_schema\') and table_schema not like \'pg_temp_%\''
_table_order_by: str = 'table_catalog, table_schema, table_name'

_table_metadata_all: str = \
    'database_name, schema_name, table_name, table_type, table_owner, table_creation_time, view_ddl'
_table_table_all: str = 'pg_catalog.svv_all_tables ' \
                        'where schema_name not in (\'pg_toast\', \'pg_internal\', \'catalog_history\', ' \
                        '\'pg_catalog\', \'information_schema\') ' \
                        'and schema_name not like \'pg_temp_%\''
_table_order_by_all: str = 'database_name, schema_name, table_name'

_table_metadata_redshift: str = 'database_name, schema_name, table_name, table_type, table_acl, remarks'
_table_table_redshift: str = 'pg_catalog.svv_redshift_tables ' \
                             'where schema_name not in (\'pg_toast\', \'pg_internal\', \'catalog_history\', ' \
                             '\'pg_catalog\', \'information_schema\') ' \
                             'and schema_name not like \'pg_temp_%\''
_table_order_by_redshift: str = 'database_name, schema_name, table_name'

_table_metadata_external: str = \
    'databasename, schemaname, tablename, location, input_format, output_format, serialization_lib, ' \
    'serde_parameters, compressed, parameters, tabletype'
_table_select_external: str = \
    '(current_database())::character varying(128) as databasename, ' \
    'schemaname, tablename, location, input_format, output_format, serialization_lib, ' \
    'serde_parameters, compressed, parameters, tabletype'
_table_table_external: str = 'pg_catalog.svv_external_tables ' \
                             'where schemaname not in (\'pg_toast\', \'pg_internal\', \'catalog_history\', ' \
                             '\'pg_catalog\', \'information_schema\') ' \
                             'and schemaname not like \'pg_temp_%\''
_table_order_by_external: str = 'schemaname, tablename'

_table_metadata_info: str = \
    'database, schema, table_id, table, encoded, diststyle, sortkey1, max_varchar, sortkey1_enc, sortkey_num, ' \
    'size, pct_used, empty, unsorted, stats_off, tbl_rows, skew_sortkey1, skew_rows, estimated_visible_rows, ' \
    'risk_event, vacuum_sort_benefit'
_table_select_info: str = \
    'database, schema, table_id, "table", encoded, diststyle, ' \
    'sortkey1, max_varchar, trim(sortkey1_enc) sortkey1_enc, sortkey_num, ' \
    'size, pct_used, empty, unsorted, stats_off, tbl_rows, skew_sortkey1, skew_rows, estimated_visible_rows, ' \
    'risk_event, vacuum_sort_benefit'
_table_table_info: str = 'pg_catalog.svv_table_info ' \
                         'where schema not in (\'pg_toast\', \'pg_internal\', \'catalog_history\', ' \
                         '\'pg_catalog\', \'information_schema\') ' \
                         'and schema not like \'pg_temp_%\''
_table_order_by_info: str = 'database, schema, "table"'

_column_metadata: str = \
    'database_name, schema_name, table_name, column_name, ordinal_position, column_default, is_nullable, ' \
    'data_type, character_maximum_length, numeric_precision, numeric_scale, remarks'
_column_table: str = 'pg_catalog.svv_all_columns ' \
                     'where schema_name not in (\'pg_toast\', \'pg_internal\', \'catalog_history\', ' \
                     '\'pg_catalog\', \'information_schema\') ' \
                     'and schema_name not like \'pg_temp_%\''
_column_order_by: str = f'database_name, schema_name, table_name, ordinal_position'

_column_metadata_redshift: str = \
    'database_name, schema_name, table_name, column_name, ordinal_position, ' \
    'data_type, column_default, is_nullable, encoding, distkey, sortkey, column_acl, remarks'
_column_table_redshift: str = 'pg_catalog.svv_redshift_columns ' \
                              'where schema_name not in (\'pg_toast\', \'pg_internal\', \'catalog_history\', ' \
                              '\'pg_catalog\', \'information_schema\') ' \
                              'and schema_name not like \'pg_temp_%\''
_column_order_by_redshift: str = f'database_name, schema_name, table_name, ordinal_position'

_column_metadata_external: str = \
    'databasename, schemaname, tablename, columnname, external_type, columnnum, part_key, is_nullable'
_column_select_external: str = \
    '(current_database())::character varying(128) as databasename, ' \
    'schemaname, tablename, columnname, external_type, columnnum, part_key, is_nullable'
_column_table_external: str = 'pg_catalog.svv_external_columns ' \
                              'where schemaname not in (\'pg_toast\', \'pg_internal\', \'catalog_history\', ' \
                              '\'pg_catalog\', \'information_schema\') ' \
                              'and schemaname not like \'pg_temp_%\''
_column_order_by_external: str = f'schemaname, tablename, columnnum'

_function_metadata: str = 'database_name, schema_name, function_name, function_type, argument_type, result_type, prosrc'
_function_table: str = 'pg_catalog.svv_redshift_functions'
_function_order_by: str = 'database_name, schema_name, function_name'

_call_metadata: str = \
    'userid, session_userid, query, label, xid, pid, database, querytxt, starttime, endtime, aborted, from_sp_call'
_call_select: str = \
    'userid, session_userid, query, label, xid, pid, trim(database) as database, trim(querytxt) as querytxt, ' \
    'starttime, endtime, aborted, from_sp_call'
_call_table: str = 'pg_catalog.svl_stored_proc_call'
_call_order_by: str = 'starttime'

MetadataNamedtuple = namedtuple('MetadataNamedtuple', _table_metadata)
MetadataNamedtupleAll = namedtuple('MetadataNamedtupleAll', _table_metadata_all)
MetadataNamedtupleRedshift = namedtuple('MetadataNamedtupleRedshift', _table_metadata_redshift)
MetadataNamedtupleExternal = namedtuple('MetadataNamedtupleExternal', _table_metadata_external)
MetadataNamedtupleInfo = namedtuple('MetadataNamedtupleInfo', _table_metadata_info)

ColumnMetadataNamedtuple = namedtuple('ColumnMetadataNamedtuple', _column_metadata)
ColumnMetadataNamedtupleRedshift = namedtuple('ColumnMetadataNamedtupleRedshift', _column_metadata_redshift)
ColumnMetadataNamedtupleExternal = namedtuple('ColumnMetadataNamedtupleExternal', _column_metadata_external)

FunctionMetadataNamedtuple = namedtuple('FunctionMetadataNamedtuple', _function_metadata)
CallMetadataNamedtuple = namedtuple('CallMetadataNamedtuple', _call_metadata)

MetadataNamedtuple_QUERY = f'select {_table_metadata} from {_table_table} order by {_table_order_by}'

MetadataNamedtupleAll_QUERY = '''
select (current_database())::character varying(128)             as database_name
     , n.nspname                                                as schema_name
     , c.relname                                                as table_name
     , case when c.relkind = 'v' then 'VIEW' else 'TABLE' end   as table_type
     , pg_get_userbyid(c.relowner)                              as table_owner
     , relcreationtime                                          as table_creation_time
     , case
           when relkind = 'v' then
               coalesce(pg_get_viewdef(c.reloid, true), '') end as view_ddl
from pg_catalog.pg_class_info c
         left join pg_catalog.pg_namespace n on n.oid = c.relnamespace
where c.relkind in ('r', 'v')
  and n.nspname not like 'pg_temp_%'
  and n.nspname not in ('pg_toast', 'pg_internal', 'catalog_history', 'pg_catalog', 'information_schema')
order by n.nspname, c.relname
'''

MetadataNamedtupleRedshift_QUERY = \
    f'select {_table_metadata_redshift} from {_table_table_redshift} order by {_table_order_by_redshift}'
MetadataNamedtupleExternal_QUERY = \
    f'select {_table_select_external} from {_table_table_external} order by {_table_order_by_external}'
MetadataNamedtupleInfo_QUERY = f'select {_table_select_info} from {_table_table_info} order by {_table_order_by_info}'

ColumnMetadataNamedtuple_QUERY = f'select {_column_metadata} from {_column_table} order by {_column_order_by}'
ColumnMetadataNamedtupleRedshift_QUERY = \
    f'select {_column_metadata_redshift} from {_column_table_redshift} order by {_column_order_by_redshift}'
ColumnMetadataNamedtupleExternal_QUERY = \
    f'select {_column_select_external} from {_column_table_external} order by {_column_order_by_external}'

CallMetadataNamedtuple_QUERY = f'select {_call_select} from {_call_table} order by {_call_order_by}'
