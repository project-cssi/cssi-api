from flask import Blueprint, jsonify, request
from app.models import Application, ApplicationType, ApplicationSchema, Genre
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
    app_type = ApplicationType.query.filter_by(name=request.json['app_type']).first()
    description = request.json['description']
    genre = Genre.query.filter_by(name=request.json['genre']).first()

    new_application = Application(name=name, app_type=app_type, description=description, genre=genre)

    db.session.add(new_application)
    db.session.commit()

    result = application_schema.dump(new_application).data

    return jsonify({"message": "Created new application {}.".format(name), "data": result})
