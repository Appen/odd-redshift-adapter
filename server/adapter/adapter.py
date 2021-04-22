import logging
import psycopg2
from psycopg2 import sql
from odd_contract.models import DataEntity
from adapter import \
    _ADAPTER_PREFIX, _DEFAULT_CLOUD_PREFIX, MetadataTables, MetadataColumns, \
    MetadataNamedtuple_QUERY, MetadataNamedtupleAll_QUERY, MetadataNamedtupleRedshift_QUERY, \
    MetadataNamedtupleExternal_QUERY, MetadataNamedtupleInfo_QUERY, \
    ColumnMetadataNamedtuple_QUERY, ColumnMetadataNamedtupleRedshift_QUERY, \
    ColumnMetadataNamedtupleExternal_QUERY
from adapter.table import _map_table
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

            mcolumns: MetadataColumns = MetadataColumns(
                self.__execute(ColumnMetadataNamedtuple_QUERY),
                self.__execute(ColumnMetadataNamedtupleRedshift_QUERY),
                self.__execute(ColumnMetadataNamedtupleExternal_QUERY))

            self.__disconnect()
            logging.info(f'Load {len(mtables.items)} Datasets DataEntities from database')

            return _map_table(self.get_data_source_oddrn(), mtables, mcolumns)
        except Exception:
            logging.error('Failed to load metadata for tables')
            logging.exception(Exception)
            self.__disconnect()
        return []

    def get_data_transformers(self) -> list[DataEntity]:
        return []

    def get_data_transformer_runs(self) -> list[DataEntity]:
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
