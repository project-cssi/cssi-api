import os

from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app.applications import Application
from config import config

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disabling sqlalchemy event system

    config[config_name].init_app(app)

    # Set up extensions
    db.init_app(app)

    api_bp = Blueprint('api/v1', __name__)
    api = Api(api_bp)

    # Route
    api.add_resource(Application, '/application')

    return app
