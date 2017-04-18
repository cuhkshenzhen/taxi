from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from flask_debugtoolbar import DebugToolbarExtension
# from celery import Celery
from config import config, Config
import os
import time
from .utils.macros \
    import format_date_thedaybefore, check_date, format_date, timestamp, product_has_sold, generate_timeout_token
from .utils.template import get_date_str
from .utils.template import generate_navigation_bar

toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

# Flask-Uploads
PDF = ('pdf',)


# for reading files
APP_ROOT = os.path.dirname(os.path.abspath(
    __file__))  # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    #    celery.conf.update(app.config)
    toolbar.init_app(app)

    # convert unicode to string
    app.jinja_env.filters['split'] = str.split
    app.jinja_env.filters['str'] = str
    app.jinja_env.filters['date_thedaybefore'] = format_date_thedaybefore
    app.jinja_env.filters['date'] = format_date
    app.jinja_env.filters['unix_time'] = time.mktime
    app.jinja_env.filters['product_has_sold'] = product_has_sold
    app.jinja_env.filters['date_str'] = get_date_str


    # add test equalto which is included in 2.8
    app.jinja_env.tests['equalto'] = lambda value, other: value == other
    # import function
    app.jinja_env.globals.update(check_date=check_date, generate_navigation_bar=generate_navigation_bar,
                                 timestamp=timestamp)
    #    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
    #        from flask_sslify import SSLify
    #        sslify = SSLify(app)

    @app.context_processor
    def processor():
        return {
                    'PERMANENT_SESSION_LIFETIME_MS': (app.permanent_session_lifetime.seconds * 1000),
                    'generate_timeout_token': generate_timeout_token,
                    'debug': app.debug
               }
    # Add current_app.permanent_session_lifetime converted to milliseconds
    # to context. The config variable PERMANENT_SESSION_LIFETIME is not
    # used because it could be either a timedelta object or an integer
    # representing seconds.


    from .modules.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
