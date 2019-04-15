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

import uuid
from flask import Blueprint, jsonify, request
from app.models import Application, ApplicationType, ApplicationSchema, Genre
from app import db

application = Blueprint('application', __name__)

application_schema = ApplicationSchema(strict=True)
applications_schema = ApplicationSchema(many=True, strict=True)


@application.route('/', methods=['GET'])
def get_applications():
    """Get a list of all the Applications"""
    applications = Application.query.all()
    result = applications_schema.dump(applications).data
    return jsonify({'status': 'success', 'message': None, 'data': result}), 200


@application.route('/<int:id>', methods=['GET'])
def get_application(id):
    """Get info on an Applications when an id is passed in"""
    application = Application.query.get(id)
    result = application_schema.dump(application).data
    return jsonify({'status': 'success', 'message': None, 'data': result}), 200


@application.route('/', methods=['POST'])
def create_application():
    """Create a new Application"""
    json_data = request.get_json(force=True)

    if not json_data:
        return jsonify({'status': 'error', 'message': 'No input was provided.'}), 400

    # Validate and deserialize input
    data, errors = application_schema.load(json_data)
    if errors:
        return jsonify({'status': 'error', 'message': 'Incorrect format of data provided.', 'data': errors}), 422

    name = data['name']
    identifier = str(uuid.uuid4().hex)
    developer = data['developer']
    type = ApplicationType.query.filter_by(name=data['type']).first()
    description = data['description']
    genre = Genre.query.filter_by(name=data['genre']).first()

    print(identifier)
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
