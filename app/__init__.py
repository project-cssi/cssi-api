import os
import logging.config

from celery import Celery
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO

from config import CONFIG

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_FILES_PATH = os.path.split(BASE_DIR)[0] + '/logs'

# Try to create a log folder
try:
    if not os.path.exists(LOG_FILES_PATH):
        os.makedirs(LOG_FILES_PATH)
except OSError:
    pass

# Load logging config file
logging.config.fileConfig('config/logging.conf', disable_existing_loggers=False)
# Init file logger
logger = logging.getLogger('CSSI_REST_API')

db = SQLAlchemy()
ma = Marshmallow()
socketio = SocketIO()
celery = Celery(__name__,
                broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
                backend=os.environ.get('CELERY_BACKEND', 'redis://localhost:6379'))
celery.config_from_object('celeryconfig')

# Import models to register them with SQLAlchemy
from app.models import Application, Genre, ApplicationType, Session, Questionnaire


def create_app(config_name=None, main=True):
    app = Flask(__name__)
    app.config.from_object(CONFIG[config_name])

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disabling sqlalchemy event system

    CORS(app, support_credentials=True)  # Add CORS support

    CONFIG[config_name].init_app(app)

    root = CONFIG[config_name].APPLICATION_ROOT



    # Set up extensions
    db.init_app(app)

    if main:
        # Initialize socketio server and attach it to the message queue.
        socketio.init_app(app,
                          message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'])
    else:
        # Initialize socketio to emit events through through the message queue.
        socketio.init_app(None,
                          message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'],
                          async_mode='threading')

    celery.conf.update(CONFIG[config_name].CELERY_CONFIG)

    # Create app blueprints
    from app.routes.v1 import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix=root + '/')

    from app.routes.v1 import application as application_blueprint
    app.register_blueprint(application_blueprint, url_prefix=root + '/applications')

    from app.routes.v1 import session as session_blueprint
    app.register_blueprint(session_blueprint, url_prefix=root + '/sessions')

    from app.routes.v1 import questionnaire as questionnaire_blueprint
    app.register_blueprint(questionnaire_blueprint, url_prefix=root + '/questionnaires')

    return app
