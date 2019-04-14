from flask import Blueprint, jsonify

applications = Blueprint('applications', __name__)


@applications.route('/', methods=['GET'])
def get_applications():
    return jsonify({"message": "Get Application New API"})


@applications.route('/', methods=['POST'])
def create_application():
    return jsonify({"message": "Created Application New API"})
