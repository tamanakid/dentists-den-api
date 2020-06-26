from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta



basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
bcrypt = Bcrypt()
cors = CORS()


def register_extensions(app):
	app.config['JWT_SECRET_KEY'] = 'secret-key'
	app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=60)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	db.init_app(app)
	ma.init_app(app)
	jwt.init_app(app)
	bcrypt.init_app(app)
	cors.init_app(app)

