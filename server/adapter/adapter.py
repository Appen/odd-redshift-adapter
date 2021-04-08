import logging
import psycopg2
from psycopg2 import sql
from odd_contract.models import DataEntity
from adapter import \
    _ADAPTER_PREFIX, _DEFAULT_CLOUD_PREFIX, MetadataTables, MetadataColumns, \
    MetadataNamedtuple_QUERY, MetadataNamedtupleAll_QUERY, MetadataNamedtupleRedshift_QUERY, \
    MetadataNamedtupleExternal_QUERY, MetadataNamedtupleInfo_QUERY, \
    ColumnMetadataNamedtuple_QUERY, ColumnMetadataNamedtupleRedshift_QUERY, \
    ColumnMetadataNamedtupleExternal_QUERY, FunctionMetadataNamedtuple_QUERY, CallMetadataNamedtuple_QUERY, \
    ColumnMetadataNamedtuple, FieldStat_UNION, FieldStat_ORDERBY, FieldStatInteger_QUERY, FieldStatInteger_FORMAT
# from adapter.call import _map_call
# from adapter.function import _map_function
from adapter.table import _map_table
from adapter.type import TABLE_TYPES_SQL_TO_ODD, TYPES_SQL_TO_ODD
from app.abstract_adapter import AbstractAdapter


def create_adapter(data_source_name: str, data_source: str) -> AbstractAdapter:
    return RedshiftAdapter(data_source_name, data_source)


class RedshiftAdapter(AbstractAdapter):
    __cloud_prefix: str = _DEFAULT_CLOUD_PREFIX
    __connection = None
    __cursor = None

    def __init__(self, data_source_name: str, data_source: str) -> None:
        super().__init__(data_source_name, data_source)
        self.__cloud_prefix = self.__get_cloud_prefix()
        self.__data_source_oddrn = f'//{self.__cloud_prefix}{_ADAPTER_PREFIX}{self._data_source_name}'

    def get_data_source_oddrn(self) -> str:
        return self.__data_source_oddrn

    def get_datasets(self) -> list[DataEntity]:
        try:
            self.__connect()

            mtables: MetadataTables = MetadataTables(
                self.__execute(MetadataNamedtuple_QUERY),
                self.__execute(MetadataNamedtupleAll_QUERY),
                self.__execute(MetadataNamedtupleRedshift_QUERY),
                self.__execute(MetadataNamedtupleExternal_QUERY),
                self.__execute(MetadataNamedtupleInfo_QUERY))

            columns_base = self.__execute(ColumnMetadataNamedtuple_QUERY)

            query_columns: [sql.SQL] = []
            for column in columns_base:
                mcolumn = ColumnMetadataNamedtuple(*column)
                if mcolumn.data_type in TYPES_SQL_TO_ODD and TYPES_SQL_TO_ODD[mcolumn.data_type] == 'TYPE_INTEGER':
                    query_column = \
                        sql.SQL(FieldStatInteger_FORMAT if len(query_columns) == 0 else FieldStatInteger_QUERY).format(
                            schemaname=sql.Literal(mcolumn.schema_name),
                            tablename=sql.Literal(mcolumn.table_name),
                            columnname=sql.Literal(mcolumn.column_name),
                            ordinalposition=sql.Literal(mcolumn.ordinal_position),
                            column=sql.Identifier(mcolumn.column_name),
                            table=sql.Identifier(mcolumn.schema_name, mcolumn.table_name))
                    query_columns.append(query_column)
            columns_integer = {()}
            if len(query_columns) > 0:
                query_integer: sql.Composed = \
                    sql.Composed(query_columns).join(FieldStat_UNION) + sql.SQL(FieldStat_ORDERBY)
                test: str = query_integer.as_string(self.__connection)
                columns_integer = self.__execute_sql(query_integer)

            mcolumns: MetadataColumns = MetadataColumns(
                columns_base,
                self.__execute(ColumnMetadataNamedtupleRedshift_QUERY),
                self.__execute(ColumnMetadataNamedtupleExternal_QUERY),
                columns_integer)

            return _map_table(self.get_data_source_oddrn(), mtables, mcolumns)
        except Exception:
            logging.error('Failed to load metadata for tables')
            logging.exception(Exception)
        finally:
            self.__disconnect()
        return []

    def get_data_transformers(self) -> list[DataEntity]:
        # try:
        #     self.__connect()
        #
        #     functions = self.__execute(FunctionMetadataNamedtuple_QUERY)
        #
        #     return _map_function(self.get_data_source_oddrn(), functions)
        # except Exception:
        #     logging.error('Failed to load metadata for tables')
        #     logging.exception(Exception)
        # finally:
        #     self.__disconnect()
        return []

    def get_data_transformer_runs(self) -> list[DataEntity]:
        # try:
        #     self.__connect()
        #
        #     calls = self.__execute(CallMetadataNamedtuple_QUERY)
        #
        #     return _map_call(self.get_data_source_oddrn(), calls)
        # except Exception:
        #     logging.error('Failed to load metadata for tables')
        #     logging.exception(Exception)
        # finally:
        #     self.__disconnect()
        return []

    def __get_cloud_prefix(self) -> str:
        if self.__cloud_prefix == _DEFAULT_CLOUD_PREFIX:
            try:
                self.__connect()

                records = self.__execute('select current_aws_account')
                if len(records) == 1:
                    self.__cloud_prefix = f'aws/{records[0][0]}/'

            except Exception:
                logging.error('Failed to get AWS account')
                logging.exception(Exception)
            finally:
                self.__disconnect()

        return self.__cloud_prefix

    def __query(self, columns: str, table: str, order_by: str) -> list[tuple]:
        return self.__execute(f'select {columns} from {table} order by {order_by}')

    def __execute(self, query: str) -> list[tuple]:
        self.__cursor.execute(query)
        records = self.__cursor.fetchall()
        return records

    def __execute_sql(self, query: sql.Composed) -> list[tuple]:
        self.__cursor.execute(query)
        records = self.__cursor.fetchall()
        return records

    def __connect(self):
        try:
            self.__connection = psycopg2.connect(self._data_source)
            self.__cursor = self.__connection.cursor()

        except psycopg2.Error as err:
            logging.error(err)
            raise DBException('Database error')
        return

    def __disconnect(self):
        try:
            if self.__cursor:
                self.__cursor.close()
        except Exception:
            pass
        try:
            if self.__connection:
                self.__connection.close()
        except Exception:
            pass
        return


class DBException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
