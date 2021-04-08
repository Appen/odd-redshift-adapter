import os
import logging
from typing import Any


class MissingEnvironmentVariable(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


def get_env(env: str, default_value: Any = None) -> str:
    try:
        return os.environ[env]
    except KeyError:
        if default_value is not None:
            return default_value
        raise MissingEnvironmentVariable(f'{env} does not exist')


class BaseConfig:
    ODD_HOST = get_env('PGHOST', get_env('ODD_DATA_SOURCE_NAME', 'localhost'))
    ODD_PORT = get_env('PGPORT', '5439')
    ODD_DATABASE = get_env('PGDATABASE', '')
    ODD_USER = get_env('PGUSER', '')
    ODD_PASSWORD = get_env('PGPASSWORD', '')

    ODD_DATA_SOURCE_NAME = get_env('ODD_DATA_SOURCE_NAME', get_env('PGHOST', 'localhost'))
    ODD_DATA_SOURCE = get_env('ODD_DATA_SOURCE', 'postgresql://')

    SCHEDULER_INTERVAL_MINUTES = get_env('SCHEDULER_INTERVAL_MINUTES', 60)


class DevelopmentConfig(BaseConfig):
    FLASK_DEBUG = True


class ProductionConfig(BaseConfig):
    FLASK_DEBUG = True


def log_env_vars(config: dict):
    logging.info('Environment variables:')
    logging.info(f'ODD_DATA_SOURCE_NAME={config["ODD_DATA_SOURCE_NAME"]}')
    logging.info(f'ODD_DATA_SOURCE={config["ODD_DATA_SOURCE"]}')
    logging.info(f'PGHOST={config["ODD_HOST"]}')
    logging.info(f'PGPORT={config["ODD_PORT"]}')
    logging.info(f'PGDATABASE={config["ODD_DATABASE"]}')
    logging.info(f'PGUSER={config["ODD_USER"]}')
    if config["ODD_PASSWORD"] != '':
        logging.info('PGPASSWORD=***')
    logging.info(f'SCHEDULER_INTERVAL_MINUTES={config["SCHEDULER_INTERVAL_MINUTES"]}')
