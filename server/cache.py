from datetime import datetime
from itertools import chain
from typing import List, Union, Iterable, Tuple

from odd_contract.models import DataEntity

RedshiftDataCacheEntry = Tuple[List[DataEntity], datetime]


class RedshiftDataCache:
    __DATA_ENTITIES: RedshiftDataCacheEntry = None
    __aws_account: str = "123456789012"

    def cache_data_entities(self,
                            aws_account: str,
                            datasets: Iterable[DataEntity],
                            data_transformers: Iterable[DataEntity],
                            data_transformer_runs: Iterable[DataEntity],
                            updated_at: datetime = datetime.utcnow()):
        self.__aws_account = aws_account
        self.__DATA_ENTITIES = list(chain(datasets, data_transformers, data_transformer_runs)), updated_at

    def retrieve_aws_account(self) -> str:
        return self.__aws_account

    def retrieve_data_entities(self, changed_since: datetime = None) -> Union[RedshiftDataCacheEntry, None]:
        if not self.__DATA_ENTITIES:
            return None

        data_entities_filtered = [
            de
            for de in self.__DATA_ENTITIES[0]
            if de.updated_at is None or de.updated_at >= changed_since
        ] if changed_since else self.__DATA_ENTITIES[0]

        return data_entities_filtered, self.__DATA_ENTITIES[1]
