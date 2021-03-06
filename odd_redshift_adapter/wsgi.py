import logging
import os

from odd_models.adapter import init_flask_app, init_controller

from .adapter import RedshiftAdapter
from .cache import Cache
from .config import log_env_vars
from .controller import Controller
from .scheduler import Scheduler

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)


def create_app(conf):
    app = init_flask_app()
    app.config.from_object(conf)
    log_env_vars(app.config)

    cache = Cache()
    adapter = RedshiftAdapter(app.config)
    init_controller(Controller(adapter, cache))

    with app.app_context():
        Scheduler(adapter, cache).start_scheduler(int(app.config['SCHEDULER_INTERVAL_MINUTES']))
        return app


if os.environ.get('FLASK_ENVIRONMENT') == "production":
    application = create_app('odd_redshift_adapter.config.ProductionConfig')
else:
    application = create_app('odd_redshift_adapter.config.DevelopmentConfig')
