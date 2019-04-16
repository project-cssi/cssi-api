from flask import Blueprint, jsonify
from flask_cors import cross_origin

main = Blueprint('main', __name__)


@main.route('/')
@cross_origin(supports_credentials=True)
def index():
    return jsonify({"message": "Welcome to CSSI REST API"})
