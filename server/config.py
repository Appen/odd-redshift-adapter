import os
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
