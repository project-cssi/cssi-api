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
    return jsonify({'status': 'success', 'message': None, 'data': applications}), 200


@application.route('/', methods=['POST'])
def create_application():
    json_data = request.get_json(force=True)

    if not json_data:
        return jsonify({'status': 'error', 'message': 'No input was provided.'}), 400

    # Validate and deserialize input
    data, errors = application_schema.load(json_data)
    if errors:
        return jsonify({'status': 'error', 'message': 'Incorrect format of data provided.', 'data': errors}), 422

    name = data['name']
    app_type = ApplicationType.query.filter_by(name=data['app_type']).first()
    description = data['description']
    genre = Genre.query.filter_by(name=data['genre']).first()

    # validate application type
    if not app_type:
        return {'status': 'error', 'message': 'Invalid Application Type'}, 400

    # validate genre
    if not genre:
        return {'status': 'error', 'message': 'Invalid Genre Type'}, 400

    new_application = Application(name=name, app_type=app_type, description=description, genre=genre)

    db.session.add(new_application)
    db.session.commit()

    result = application_schema.dump(new_application).data

    return jsonify({'status': 'success', 'message': 'Created new application {}.'.format(name), 'data': result}), 201
