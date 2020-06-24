from flask import request
from werkzeug.exceptions import HTTPException
from flask_restx import Namespace, Resource, fields, reqparse, marshal
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


api = Namespace("user", description="User-Related Endpoints")


user_parser = reqparse.RequestParser()
user_parser.add_argument("username", type=str, required=True)
user_parser.add_argument("firstname", type=str, required=True)
user_parser.add_argument("lastname", type=str, required=True)
user_parser.add_argument("password", type=str, required=True)



user_login = reqparse.RequestParser()
user_login.add_argument("username", type=str, required=True)
user_login.add_argument("password", type=str, required=True)

error_fields = api.model("Error_Fields",
    {
        "message": fields.String(required=False, description="Message"),
    }
)


userlogin = api.model("UserLogin",
    {
        "username": fields.String(required=True, description="The username (primary key)"),
        "password": fields.String(required=True, description="The user's password"),
    }
)


# These should api.inherit() from userlogin (https://www.youtube.com/watch?v=YvXHpBYH4yE&list=PLNmsVeXQZj7otfP2zTa8AIiNIWVg0BRqs&index=27)

user = api.model("User",
    {
        "username": fields.String(required=True, description="The username (primary key)"),
        "firstname": fields.String(required=True, description="The user's first name"),
        "lastname": fields.String(required=True, description="The user's last name(s)"),
    },
)

user_token = api.model("User_Token",
    {
        "username": fields.String(required=True, description="The username (primary key)"),
        "firstname": fields.String(required=True, description="The user's first name"),
        "lastname": fields.String(required=True, description="The user's last name(s)"),
        "token": fields.String(required=True, description="Token returned from register"),
    },
)

userpost = api.model("Userpost",
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


def throw_exception(cod):

    exceptions = {
        'userExistsException': { 'marshal': { 'message': 'User already exists' }, 'status_code': 409 }
    }

    exc = exceptions[cod]
    print(f"exc: {exc}")

    return marshal(exc['marshal'], error_fields), exc['status_code']



from extensions import db, bcrypt, ma

class User(db.Model):
    username = db.Column(db.String(16), primary_key=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    password = db.Column(db.String(32))

    def __init__(self, username, firstname, lastname, password):
        super(User, self).__init__()
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password


# Product Schema
class UserSchema(ma.Schema):
	class Meta:
		fields = ("username", "firstname", "lastname", "password")

user_schema = UserSchema()
users_schema = UserSchema(many = True)


@api.route("")
class CatList(Resource):
    @jwt_required # requires "Authorization": "Bearer <token>"
    @api.doc("list_cats", security='apikey')
    @api.marshal_list_with(user, envelope="cats") # Expected response shape (envelope wraps response into an object with the "cats" key)
    def get(self):
        """List all cats"""
        current_user = get_jwt_identity()
        print(current_user)
        return CATS

    @api.doc("add_new_user")
    @api.expect(userpost, validate=True) # Expected request shape
    @api.response(201, "User created successfully", user_token)
    @api.response(409, "User already exists", error_fields)
    # @api.marshal_with(user_token, code=201) # skip_none=True
    # @api.marshal_with(user, code=201)
    def post(self):
        try:
            args = user_parser.parse_args(request) # for input validation
            print(args)
            username = args.get('username') # request.json['username']
            existing_user = User.query.get(username)
            if (existing_user is not None):
                print(f"Error: {existing_user}")
                return throw_exception('userExistsException')
                # return marshal({ 'message': 'User already exists' }, error_fields), 409
            print(f"No error: {username}")
            firstname = args.get('firstname')
            lastname = args.get('lastname')
            password = bcrypt.generate_password_hash(args.get('password')).decode("utf-8")
            user_instance = User(username, firstname, lastname, password)
            db.session.add(user_instance)
            db.session.commit()
            access_token = create_access_token(identity=username)
            return marshal({
                "username": user_instance.username,
                "firstname": user_instance.firstname,
                "lastname": user_instance.lastname,
                "token": access_token
            }, user_token), 201
            # return { 'success': True, 'password': password, 'token': access_token }, 201
        except Exception as error:
            print(error)
            return {"error": True}, 500



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
    
    @api.doc('login')
    @api.expect(userlogin, validate=True)
    def post(self, id):
        args = user_login.parse_args(request)
        print(args)
        username = args.get('username')
        password = args.get('password')
        print(password)
        try:
            isPasswordCorrect = bcrypt.check_password_hash("$2b$12$eBCn/h3fwE0OF0Nj0SgPD.PuggFeapvEtytHk1m9pnjvTwCxxxPPC", password)
            if isPasswordCorrect:
                return { "username": username }
            else:
                return { "password": "incorrect" }, 401
        except Exception as error:
            ## Should be in "return internal_err_resp()" call7
            print(error)
            return {"error": "true"}, 500


