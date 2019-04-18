#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) Copyright 2019 Brion Mario.
# (c) This file is part of the CSSI REST API and is made available under MIT license.
# (c) For more information, see https://github.com/brionmario/cssi-api/blob/master/LICENSE.txt
# (c) Please forward any queries to the given email address. email: brion@apareciumlabs.com

"""Session routes module

This modules contains all the different routes to interact with Sessions.

Authors:
    Brion Mario

"""

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from app.models import Session, SessionSchema, Application, Questionnaire
from app import db

session = Blueprint('session', __name__)

session_schema = SessionSchema(strict=True)
sessions_schema = SessionSchema(many=True, strict=True)


@session.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_sessions_list():
    """Get a list of all the sessions"""
    sessions = Session.query.all()
    result = sessions_schema.dump(sessions).data
    return jsonify({'status': 'success', 'message': None, 'data': result}), 200


@session.route('/<int:id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_session(id):
    """Get info on a session when an id is passed in"""
    session = Session.query.get(id)
    result = sessions_schema.dump(session).data
    return jsonify({'status': 'success', 'message': None, 'data': result}), 200


@session.route('/', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_session():
    """Create a new Session"""
    app = Application.query.filter_by(id=request.json['app']).first()
    questionnaire = Questionnaire.query.filter_by(id=request.json['questionnaire']).first()
    expected_emotions = request.json['expected_emotions']

    print(questionnaire)

    # validate application type
    if not app:
        return {'status': 'error', 'message': 'Invalid application.'}, 400

    new_session = Session(app=app, expected_emotions=expected_emotions, questionnaire=questionnaire)

    db.session.add(new_session)
    db.session.commit()

    result = session_schema.dump(new_session).data

    return jsonify({'status': 'success', 'message': 'Created new session for application with id of {}.'.format(request.json['app']), 'data': result}), 201
