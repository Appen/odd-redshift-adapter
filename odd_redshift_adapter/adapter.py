import logging

import psycopg2
from odd_models.models import DataEntity
from oddrn_generator import RedshiftGenerator

from .mappers import (
    MetadataNamedtuple_QUERY, MetadataNamedtupleAll_QUERY, MetadataNamedtupleRedshift_QUERY,
    MetadataNamedtupleExternal_QUERY, MetadataNamedtupleInfo_QUERY,
    ColumnMetadataNamedtuple_QUERY, ColumnMetadataNamedtupleRedshift_QUERY,
    ColumnMetadataNamedtupleExternal_QUERY
)
from .mappers.metadata import MetadataTables, MetadataColumns
from .mappers.tables import map_table


class RedshiftAdapter:
    __connection = None
    __cursor = None

    def __init__(self, config) -> None:
        self.__host = config['ODD_HOST']
        self.__port = config['ODD_PORT']
        self.__database = config['ODD_DATABASE']
        self.__user = config['ODD_USER']
        self.__password = config['ODD_PASSWORD']

        self._data_source = f"postgresql://{self.__user}:{self.__password}@{self.__host}:{self.__port}/{self.__database}?connect_timeout=10"
        self.__oddrn_generator = RedshiftGenerator(host_settings=f"{self.__host}", databases=self.__database)

    def get_data_source_oddrn(self) -> str:
        return self.__oddrn_generator.get_data_source_oddrn()

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

            return map_table(self.__oddrn_generator, mtables, mcolumns)
        except Exception as e:
            logging.error('Failed to load metadata for tables')
            logging.exception(e)
            self.__disconnect()
        return []

    def get_data_transformers(self) -> list[DataEntity]:
        return []

    def get_data_transformer_runs(self) -> list[DataEntity]:
        return []

    def __query(self, columns: str, table: str, order_by: str) -> list[tuple]:
        return self.__execute(f'select {columns} from {table} order by {order_by}')

    def __execute(self, query: str) -> list[tuple]:
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
    pass
