#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) Copyright 2019 CSSI.
# (c) This file is part of the CSSI REST API and is made available under MIT license.
# (c) For more information, see https://github.com/project-cssi/cssi-api/blob/master/LICENSE.md
# (c) Please forward any queries to the given email address. email: opensource@apareciumlabs.com

"""Configurations for the CSSI REST API

This module handles the different configurations used in the REST API.
Config is the parent class and contains the generic config attributes.
DevelopmentConfig, TestingConfig, ProductionConfig inherits Config.

Examples:
    The module could be used as follows. config_name acn be either
    'default', 'testing', 'development' or 'production'.

    from config import config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

Attributes:
    ENVIRONMENT_FILE_NAME (str): Name of the file containing the
        environment variables.

Todo:
    * Add different configs for cloud deployments.

Authors:
    Brion Mario

"""
import logging
import os

logger = logging.getLogger('cssi.api')

ENVIRONMENT_FILE_NAME = '.env'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Read the environment file
if os.path.exists(ENVIRONMENT_FILE_NAME):
    logger.info('Importing environment from environment file')
    for line in open(ENVIRONMENT_FILE_NAME):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")


class Config:
    """The parent Config class.

        This class is the blueprint for all the config types. It should be extended
        by the other configuration types.

        Attributes:
            APP_NAME (str): Name of the app. If not declared in the environment file,
                defaults to 'CSSI_REST_API'
            SECRET_KEY (str): Secret key for the app.
            SQLALCHEMY_COMMIT_ON_TEARDOWN (bool): SQLAlchemy config to enable automatical
                db commit on teardown.

    """

    APP_NAME = os.environ.get('APP_NAME') or 'CSSI_REST_API'
    APPLICATION_ROOT = os.environ.get('APPLICATION_ROOT') or '/api/v1'
    CELERY_BROKER_URL = os.environ.get(
        'CELERY_BROKER_URL', 'redis://localhost:6379')
    CELERY_CONFIG = {}
    SOCKETIO_MESSAGE_QUEUE = os.environ.get(
        'SOCKETIO_MESSAGE_QUEUE', os.environ.get('CELERY_BROKER_URL',
                                                 'redis://'))

    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
        logger.error('Secret key is not set in the environment')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Development config class.

        This class sets the configurations required for app to run on a development
        environment. This class inherits the Config class.

        Attributes:
            DEBUG (bool): Sets if app debug is enabled or disabled.
            SQLALCHEMY_DATABASE_URI (str): Database connection string.

    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'cssi-dev.sqlite')
    CELERY_BROKER_URL = os.environ.get(
        'DEV_CELERY_BROKER_URL', 'redis://localhost:6379')
    CELERY_BACKEND = os.environ.get('DEV_CELERY_BACKEND') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'celery-dev.sqlite')

    @classmethod
    def init_app(cls, app):
        logger.info('The app is running in debug mode.')


class TestingConfig(Config):
    """Testing config class.

        This class sets the configurations required for app to run on a testing
        environment. This class inherits the Config class.

        Attributes:
            TESTING (bool): Sets if app testing is enabled or disabled.
            SQLALCHEMY_DATABASE_URI (str): Database connection string.

    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'cssi-test.sqlite')
    CELERY_BROKER_URL = os.environ.get(
        'TEST_CELERY_BROKER_URL', 'redis://localhost:6379')
    CELERY_BACKEND = os.environ.get('TEST_CELERY_BACKEND') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'celery-test.sqlite')
    CELERY_CONFIG = {'CELERY_ALWAYS_EAGER': True}
    SOCKETIO_MESSAGE_QUEUE = None

    @classmethod
    def init_app(cls, app):
        logger.info('The app is running in testing mode.')


class ProductionConfig(Config):
    """Production config class.

        This class sets the configurations required for app to run on a production
        environment. This class inherits the Config class.

        Attributes:
            SQLALCHEMY_DATABASE_URI (str): Database connection string.
            SSL_DISABLE (bool): Sets if SSL is enabled or disabled.

    """

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'cssi.sqlite')
    CELERY_BROKER_URL = os.environ.get(
        'CELERY_BROKER_URL', 'redis://localhost:6379')
    CELERY_BACKEND = os.environ.get('CELERY_BACKEND') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'celery.sqlite')
    SSL_DISABLE = (os.environ.get('SSL_DISABLE') or 'True') == 'True'

    @classmethod
    def init_app(cls, app):
        logger.info('The app is running in production mode.')
        Config.init_app(app)
        assert os.environ.get('SECRET_KEY'), 'SECRET_KEY IS NOT SET!'


CONFIG = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
