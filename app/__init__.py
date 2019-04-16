import os
import logging.config

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import CONFIG

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_FILES_PATH = os.path.split(BASE_DIR)[0] + '/logs'

# Try to create a log folder
try:
    if not os.path.exists(LOG_FILES_PATH):
        os.makedirs(LOG_FILES_PATH)
except OSError:
    pass

# load logging config file
logging.config.fileConfig('config/logging.conf', disable_existing_loggers=False)
# init file logger
logger = logging.getLogger('CSSI_REST_API')

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app, support_credentials=True)
    app.config.from_object(CONFIG[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disabling sqlalchemy event system

    CONFIG[config_name].init_app(app)

    root = CONFIG[config_name].APPLICATION_ROOT

    # flask migrate doesn't recognize the tables without this import
    from app.models import Application, Genre, ApplicationType, Session, Questionnaire

    # Set up extensions
    db.init_app(app)

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
