import os
from logging.config import dictConfig

from flask import Response
from odd_contract import init_flask_app, init_controller

from adapter import RedshiftAdapter
from cache import RedshiftDataCache
from controllers import OpenDataDiscoveryController
from scheduler import Scheduler

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def create_app(conf):
    app = init_flask_app()
    app.config.from_object(conf)

    app.add_url_rule("/health", "healthcheck", lambda: Response(status=200))

    redshift_data_cache = RedshiftDataCache()

    init_controller(
        OpenDataDiscoveryController(host_name=app.config["PGHOST"], redshift_data_cache=redshift_data_cache)
    )

    with app.app_context():
        Scheduler(
            redshift_adapter=RedshiftAdapter(app.config["PGHOST"]),
            redshift_data_cache=redshift_data_cache
        ).start_scheduler(interval_minutes=int(app.config["SCHEDULER_INTERVAL_MINUTES"]))

        return app


application = create_app(os.environ.get("FLASK_CONFIG") or "config.DevelopmentConfig")
