#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) Copyright 2019 Brion Mario.
# (c) This file is part of the CSSI REST API and is made available under MIT license.
# (c) For more information, see https://github.com/brionmario/cssi-api/blob/master/LICENSE.txt
# (c) Please forward any queries to the given email address. email: brion@apareciumlabs.com

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

import os

ENVIRONMENT_FILE_NAME = '.env'

basedir = os.path.abspath(os.path.dirname(__file__))

# Read the environment file
if os.path.exists(ENVIRONMENT_FILE_NAME):
    print('Importing environment from environment file')
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

    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
        print('SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION')
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
                              'sqlite:///' + os.path.join(basedir, 'cssi-dev.sqlite')

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


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
                              'sqlite:///' + os.path.join(basedir, 'cssi-test.sqlite')

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN TESTING MODE.  \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class ProductionConfig(Config):
    """Production config class.

        This class sets the configurations required for app to run on a production
        environment. This class inherits the Config class.

        Attributes:
            SQLALCHEMY_DATABASE_URI (str): Database connection string.
            SSL_DISABLE (bool): Sets if SSL is enabled or disabled.

    """

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'cssi.sqlite')
    SSL_DISABLE = (os.environ.get('SSL_DISABLE') or 'True') == 'True'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert os.environ.get('SECRET_KEY'), 'SECRET_KEY IS NOT SET!'


CONFIG = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
