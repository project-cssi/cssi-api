from flask import Flask
from app.routes import *

app = Flask(__name__)

app.run(debug=True)
