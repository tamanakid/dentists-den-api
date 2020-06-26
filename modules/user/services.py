from flask_restx import marshal
from flask_jwt_extended import create_access_token#, jwt_required, get_jwt_identity

from extensions import db, bcrypt
from .models_db import *
from .models_api import *
from .exceptions import *



class AuthService:

	def register(body):
		# Parse body
		username = body.get('username') # request.json['username']
		firstname = body.get('firstname')
		lastname = body.get('lastname')
		password = bcrypt.generate_password_hash(body.get('password')).decode("utf-8")

		# Check if username already exists
		existing_user = User.query.get(username)
		if (existing_user is not None):
			print(f"Existing user: {existing_user}")
			return throw_exception(USER_REGISTER_EXISTS)

		access_token = create_access_token(identity=username)

		# Instantiate user and save in DDBB
		user_instance = User(username, firstname, lastname, password)
		db.session.add(user_instance)
		db.session.commit()


		return marshal({
			"username": user_instance.username,
			"firstname": user_instance.firstname,
			"lastname": user_instance.lastname,
			"token": access_token
		}, user_wtoken_model), 201