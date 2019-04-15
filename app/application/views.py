from flask import Blueprint, jsonify, request
from app.models import Application, ApplicationType, ApplicationSchema
from marshmallow import Schema, fields, ValidationError, pre_load
from .. import db

application = Blueprint('application', __name__)

applications_schema = ApplicationSchema(many=True)
application_schema = ApplicationSchema()


@application.route('/', methods=['GET'])
def get_applications():
    applications = Application.query.all()
    applications = applications_schema.dump(applications).data
    return jsonify({"status": "success", "data": applications}), 200


@application.route('/', methods=['POST'])
def create_application():
    name = request.json['name']
    type_id = request.json['type_id']
    description = request.json['description']
    genre_id = request.json['genre_id']

    new_application = Application(name=name, type_id=type_id, description=description, genre_id=genre_id)

    db.session.add(new_application)
    db.session.commit()

    result = application_schema.dump(new_application).data

    return jsonify({"message": "Created new application {}.".format(name), "data": result})
