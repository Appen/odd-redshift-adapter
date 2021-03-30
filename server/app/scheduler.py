import logging
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.abstract_adapter import AbstractAdapter
from app.cache import Cache


class Scheduler:
    def __init__(self, adapter: AbstractAdapter, cache: Cache) -> None:
        self.__adapter = adapter
        self.__cache = cache
        self.__scheduler = BackgroundScheduler(executors={'default': ThreadPoolExecutor(1)})

    def start_scheduler(self, interval_minutes: int):
        self.__scheduler.start()
        self.__scheduler.add_job(self.__retrieve_data_entities,
                                 trigger='interval',
                                 minutes=interval_minutes,
                                 next_run_time=datetime.now())

    def __retrieve_data_entities(self):
        datasets = self.__adapter.get_datasets()
        data_transformers = self.__adapter.get_data_transformers()
        data_transformer_runs = self.__adapter.get_data_transformer_runs()
        self.__cache.cache_data_entities(
            datasets,
            data_transformers,
            data_transformer_runs)
        logging.info(f'Put {len(datasets)} Datasets, '
                     f'{len(data_transformers)} DataTransformers, '
                     f'{len(data_transformer_runs)} DataTransformerRuns '
                     f'DataEntities to cache from database')
