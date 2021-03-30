from abc import ABC, abstractmethod
from odd_contract.models import DataEntity


class AbstractAdapter(ABC):
    def __init__(self, data_source_name: str, data_source: str) -> None:
        self._data_source_name = data_source_name
        self._data_source = data_source
        super().__init__()

    @abstractmethod
    def get_data_source_oddrn(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_datasets(self) -> list[DataEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_data_transformers(self) -> list[DataEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_data_transformer_runs(self) -> list[DataEntity]:
        raise NotImplementedError

# def init_adapter(controller: AbstractAdapter):
#     AdapterHolder.init_adapter(controller)
#
#
# def get_adapter() -> AbstractAdapter:
#     return AdapterHolder.get_adapter()
#
#
# class AdapterHolder:
#     __adapter: AbstractAdapter = None
#
#     @classmethod
#     def init_adapter(cls, controller: AbstractAdapter):
#         cls.__adapter = controller
#
#     @classmethod
#     def get_adapter(cls) -> AbstractAdapter:
#         if cls.__adapter is None:
#             raise RuntimeError('ODD adapter has never been initialized')
#         return cls.__adapter
