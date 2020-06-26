from flask_restx import fields, reqparse

from . import ns
from utils.error_handling import append_error_fields

error_fields = append_error_fields(ns)


# Register base

# Unable to inherit
# user_register_base = ns.model("user_register_model", {
# 	"username": fields.String(required=True, description="The username (primary key)"),
# 	"firstname": fields.String(required=True, description="The user's first name"),
# 	"lastname": fields.String(required=True, description="The user's last name(s)"),
# })


# Register request

user_register_parser = reqparse.RequestParser()
user_register_parser.add_argument("username", type=str, required=True)
user_register_parser.add_argument("firstname", type=str, required=True)
user_register_parser.add_argument("lastname", type=str, required=True)
user_register_parser.add_argument("password", type=str, required=True)

user_register_model = ns.model("user_register_model", {
	"username": fields.String(required=True, description="The username (primary key)"),
	"firstname": fields.String(required=True, description="The user's first name"),
	"lastname": fields.String(required=True, description="The user's last name(s)"),
	"password": fields.String(required=True, description="The user's password"),
})

# Register response

user_wtoken_model = ns.model("user_wtoken_model", {
	"username": fields.String(required=True, description="The username (primary key)"),
	"firstname": fields.String(required=True, description="The user's first name"),
	"lastname": fields.String(required=True, description="The user's last name(s)"),
	"token": fields.String(required=True, description="Token returned from register"),
})




# Login

user_login_parser = reqparse.RequestParser()
user_login_parser.add_argument("username", type=str, required=True)
user_login_parser.add_argument("password", type=str, required=True)

user_login_model = ns.model("user_login_model", {
	"username": fields.String(required=True, description="The username (primary key)"),
	"password": fields.String(required=True, description="The user's password"),
})
