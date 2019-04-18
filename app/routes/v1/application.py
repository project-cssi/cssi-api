#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) Copyright 2019 Brion Mario.
# (c) This file is part of the CSSI REST API and is made available under MIT license.
# (c) For more information, see https://github.com/brionmario/cssi-api/blob/master/LICENSE.txt
# (c) Please forward any queries to the given email address. email: brion@apareciumlabs.com

"""Application routes module

This modules contains all the different routes to interact with applications.

Authors:
    Brion Mario

"""

import logging
import uuid
import traceback
from flask_cors import cross_origin
from flask import Blueprint, jsonify, request
from app.models import Application, ApplicationType,ApplicationTypeSchema, ApplicationSchema, Genre, GenreSchema
from app import db

logger = logging.getLogger('CSSI_REST_API')

application = Blueprint('application', __name__)

application_schema = ApplicationSchema(strict=True)
applications_schema = ApplicationSchema(many=True, strict=True)
application_types_schema = ApplicationTypeSchema(many=True, strict=True)
application_genres_schema = GenreSchema(many=True, strict=True)


@application.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_application_list():
    """Get a list of all the Applications"""
    applications = Application.query.all()
    result = applications_schema.dump(applications).data
    return jsonify({'status': 'success', 'message': None, 'data': result}), 200


@application.route('/<int:id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_application(id):
    """Get info on an Applications when an id is passed in"""
    application = Application.query.get(id)
    result = application_schema.dump(application).data
    return jsonify({'status': 'success', 'message': None, 'data': result}), 200


@application.route('/types', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_application_types():
    """Get all the available application types"""
    application_types = ApplicationType.query.all()
    result = application_types_schema.dump(application_types).data
    return jsonify({'status': 'success', 'message': None, 'data': result}), 200


@application.route('/genres', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_application_genres():
    """Get all the available application genres"""
    application_genres = Genre.query.all()
    result = application_genres_schema.dump(application_genres).data
    return jsonify({'status': 'success', 'message': None, 'data': result}), 200


@application.route('/', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_application():
    """Create a new Application"""
    name = request.json['name']
    identifier = str(uuid.uuid4().hex)
    developer = request.json['developer']
    type = ApplicationType.query.filter_by(id=request.json['type']).first()
    description = request.json['description']
    genre = Genre.query.filter_by(id=request.json['genre']).first()

    # validate application type
    if not type:
        return {'status': 'error', 'message': 'Invalid Application Type'}, 400

    # validate genre
    if not genre:
        return {'status': 'error', 'message': 'Invalid Genre Type'}, 400

    new_application = Application(name=name, identifier=identifier, developer=developer, type=type, description=description, genre=genre)

    db.session.add(new_application)
    db.session.commit()

    result = application_schema.dump(new_application).data

    return jsonify({'status': 'success', 'message': 'Created new application {}.'.format(name), 'data': result}), 201


@application.after_request
def after_request(response):
    """Logs a debug message on every successful request."""
    logger.debug('%s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response


@application.errorhandler(Exception)
def exceptions(e):
    """Logs an error message and stacktrace if a request ends in error."""
    tb = traceback.format_exc()
    logger.error('%s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', request.remote_addr, request.method, request.scheme, request.full_path, tb)
    return e.status_code
