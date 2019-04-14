import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import CONFIG

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(CONFIG[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disabling sqlalchemy event system

    CONFIG[config_name].init_app(app)
    root = CONFIG[config_name].APPLICATION_ROOT

    # Set up extensions
    db.init_app(app)

    # Create app blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix=root + '/')

    from .applications import applications as applications_blueprint
    app.register_blueprint(applications_blueprint, url_prefix=root + '/applications')

    return app
