#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) Copyright 2019 CSSI.
# (c) This file is part of the CSSI REST API and is made available under MIT license.
# (c) For more information, see https://github.com/project-cssi/cssi-api/blob/master/LICENSE.md
# (c) Please forward any queries to the given email address. email: opensource@apareciumlabs.com

"""Session routes module

This modules contains all the different routes to interact with Sessions.

Authors:
    Brion Mario

"""

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from app.models import Session, SessionSchema, Application, Questionnaire
from app import db

from app import cssi

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
    result = session_schema.dump(session).data
    return jsonify({'status': 'success', 'message': None, 'data': result}), 200


@session.route('/<int:id>', methods=['PUT'])
@cross_origin(supports_credentials=True)
def update_session(id):
    """Update information when the session comes to an end."""
    session = Session.query.get(id)

    # calculate all the final scores of the contributors
    latency_score = cssi.latency.generate_final_score(scores=session.latency_scores)
    sentiment_score = cssi.sentiment.generate_final_score(all_emotions=session.sentiment_scores, expected_emotions=session.expected_emotions)
    questionnaire_score = cssi.questionnaire.generate_final_score(pre=session.questionnaire.pre, post=session.questionnaire.post)

    # calculate the final scores of the plugins
    plugin_scores = cssi.generate_plugin_final_scores(scores=session.plugin_scores)

    # calculate the final CSSI Score
    cssi_score = cssi.generate_cssi_score(tl=latency_score, ts=sentiment_score, tq=questionnaire_score, ps=plugin_scores)

    # set the scores in the session
    session.total_latency_score = latency_score
    session.total_sentiment_score = sentiment_score
    session.total_questionnaire_score = questionnaire_score
    session.total_plugin_scores = plugin_scores
    session.cssi_score = cssi_score

    # get a breakdown of the questionnaire scores and set it in the session
    [pre_n, pre_o, pre_d, pre_ts], [post_n, post_o, post_d, post_ts] = cssi.questionnaire.generate_score_breakdown(pre=session.questionnaire.pre, post=session.questionnaire.post)
    q_score_breakdown = {
        "pre": {
            "N": pre_n,
            "O": pre_o,
            "D": pre_d,
            "TS": pre_ts
        },
        "post": {
            "N": post_n,
            "O": post_o,
            "D": post_d,
            "TS": post_ts
        }
    }
    session.questionnaire_scores = q_score_breakdown

    session.status = "completed"
    db.session.commit()

    result = session_schema.dump(session).data

    return jsonify({'status': 'success', 'message': 'Successfully updated the session data', 'data': result}), 200


@session.route('/<int:id>/status', methods=['PATCH'])
@cross_origin(supports_credentials=True)
def update_session_status(id):
    """Update session status"""
    session = Session.query.get(id)
    session.status = request.json['status']
    db.session.commit()
    result = session_schema.dump(session).data
    return jsonify({'status': 'success', 'message': 'Successfully update the session status', 'data': result}), 200


@session.route('/', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_session():
    """Create a new Session"""
    app = Application.query.filter_by(id=request.json['app']).first()
    questionnaire = Questionnaire.query.filter_by(id=request.json['questionnaire']).first()
    expected_emotions = request.json['expected_emotions']

    # validate application type
    if not app:
        return {'status': 'error', 'message': 'Invalid application.'}, 400

    new_session = Session(app=app, expected_emotions=expected_emotions, questionnaire=questionnaire)

    db.session.add(new_session)
    db.session.commit()

    result = session_schema.dump(new_session).data

    return jsonify({'status': 'success', 'message': 'Created new session for application with id of {}.'.format(request.json['app']), 'data': result}), 201
