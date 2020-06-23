from flask import request
from flask_restx import Namespace, Resource, fields, reqparse

from token_auth import token_required


api = Namespace("user", description="User-Related Endpoints")

user_parser = reqparse.RequestParser()
user_parser.add_argument("username", type=str, required=True)
user_parser.add_argument("firstname", type=str, required=True)
user_parser.add_argument("lastname", type=str, required=True)
user_parser.add_argument("password", type=str, required=True)



user = api.model("User",
    {
        "username": fields.String(required=True, description="The username (primary key)"),
        "firstname": fields.String(required=True, description="The user's first name"),
        "lastname": fields.String(required=True, description="The user's last name(s)"),
    },
)

userpost = api.model("User",
    {
        "username": fields.String(required=True, description="The username (primary key)"),
        "firstname": fields.String(required=True, description="The user's first name"),
        "lastname": fields.String(required=True, description="The user's last name(s)"),
        "password": fields.String(required=True, description="The user's password"),
    },
)

CATS = [
    {"username": "1", "firstname": "Felix", "lastname": "Ubago", "age": 25},
    {"username": "2", "firstname": "Apolo", "lastname": "Lobato Mejia", "age": 1},
]


from app import db, bcrypt

class User(db.Model):
    username = db.Column(db.String(16), primary_key=True)
    firstname = db.Column(db.String(32), primary_key=True)
    lastname = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(32), primary_key=True)

    def __init__(self, username, firstname, lastname, password):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password



@api.route("/")
class CatList(Resource):
    @api.doc("list_cats", security='apikey')
    @token_required
    @api.marshal_list_with(user, envelope="cats") # Expected response shape (envelope wraps response into an object with the "cats" key)
    def get(self):
        """List all cats"""
        return CATS

    @api.doc("add_new_user")
    @api.expect(user_parser, validate=True) # Expected request shape
    # @api.marshal_with(user, code=201)
    def post(self):
        print(f"api payload: {request.json}")
        args = user_parser.parse_args(request) # for input validation
        print(args)
        username = args.get('username') # request.json['username']
        firstname = args.get('firstname')
        lastname = args.get('lastname')
        password = bcrypt.generate_password_hash(args.get('password')).decode("utf-8")
        # user_instance = User(username, firstname, lastname, password)
        # db.session.commit()
        # return user_instance
        return { 'success': True, 'password': password }
        '''
        login_data = request.get_json()
        print(f"login data: {login_data}")
        username = request.json['username']
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        password = request.json['password']
        print(request)
        user = User(username, firstname, lastname, password)
        db.session.commit()
        return user
        '''
                



@api.route("/<id>")
@api.param("id", "The cat identifier")
@api.response(404, "Cat not found")
class Cat(Resource):
    @api.doc("get_cat")
    @api.marshal_with(user) # Expected response shape
    def get(self, id):
        """Fetch a cat given its identifier"""
        for cat in CATS:
            if cat["id"] == int(id):
                return cat
        api.abort(404)


