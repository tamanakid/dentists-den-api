from flask import Flask, Blueprint, request
from flask_restx import Resource, Api

from extensions import register_extensions
from user import api as user_api
from dog import api as dog_api

## Instantiate Flask App

app = Flask(__name__)
app.config['SWAGGER_UI_JSONEDITOR'] = True
app.config["PROPAGATE_EXCEPTIONS"] = False

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




register_extensions(app)

## Add Namespaces

api.add_namespace(user_api)
api.add_namespace(dog_api)



## Run Application

if __name__ == '__main__':
    app.run(debug=True)



'''
To create DB formatted according to the existing Schemas:

1. Execute python
2. >>> form app import db
3. >>> db.create_all()
'''