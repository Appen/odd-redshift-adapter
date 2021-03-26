import logging

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from adapter import RedshiftAdapter
from cache import RedshiftDataCache


class Scheduler:
    def __init__(self, redshift_adapter: RedshiftAdapter, redshift_data_cache: RedshiftDataCache) -> None:
        self.__redshift_adapter = redshift_adapter
        self.__scheduler = BackgroundScheduler(executors={"default": ThreadPoolExecutor(1)})
        self.__redshift_data_cache = redshift_data_cache

    def start_scheduler(self, interval_minutes: int):
        self.__scheduler.start()
        self.__scheduler.add_job(self.__retrieve_data_entities_data,
                                 trigger="interval",
                                 minutes=interval_minutes,
                                 next_run_time=datetime.now())

    def __retrieve_data_entities_data(self):
        datasets = self.__redshift_adapter.get_datasets()
        self.__redshift_data_cache.cache_data_entities(
            self.__redshift_adapter.get_aws_account(),
            datasets,
            [],
            []
        )
        logging.info(f"Put {len(datasets)} DataEntities from PostgreSQL to cache")
