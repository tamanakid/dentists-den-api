from flask import Flask, Blueprint, request
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os

from user import api as user_api
from dog import api as dog_api

basedir = os.path.abspath(os.path.dirname(__file__))

## Instantiate Flask App

app = Flask(__name__)
app.config['SWAGGER_UI_JSONEDITOR'] = True

## authentication

autho = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


blueprint = Blueprint('swagger_api', __name__, url_prefix="/api")
api = Api(blueprint, authorizations=autho, doc="/documentation", title="The Dentist's Den API", version="1.0.0") # doc=False
app.register_blueprint(blueprint)

## api.init_app(app)

## Instantiate DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

## Extra Config
bcrypt = Bcrypt(app)
cors = CORS(app)



## Add Namespaces

api.add_namespace(user_api)
api.add_namespace(dog_api)



## Run Application

if __name__ == '__main__':
    app.run(debug=True)