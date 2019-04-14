from flask import Blueprint, jsonify

application = Blueprint('application', __name__)


@application.route('/', methods=['GET'])
def get_applications():
    return jsonify({"message": "Get Application New API"})


@application.route('/', methods=['POST'])
def create_application():
    return jsonify({"message": "Created Application New API"})
