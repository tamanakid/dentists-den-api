from flask import request
from werkzeug.exceptions import HTTPException
from flask_restx import Namespace, Resource, fields, reqparse, marshal
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from extensions import db, bcrypt



ns = Namespace("user", description="User-Related Endpoints")


from utils.exceptions_global import GLOBAL_SERVER_ERROR
from .exceptions import *
from .services import *



@ns.route("/register")
class UserRegister(Resource):

    # POST
    @ns.expect(user_register_model, validate=True)
    @ns.response(201, "User registered successfully", user_wtoken_model)
    @ns.response(409, "Username already exists", error_fields)
    def post(self):
        # try:
        body = user_register_parser.parse_args(request)
        return AuthService.register(body)
        # except Exception as error:
        #     print(f"error: {error}")
        #     return throw_exception(GLOBAL_SERVER_ERROR)



CATS = [
    {"username": "1", "firstname": "Felix", "lastname": "Ubago", "age": 25},
    {"username": "2", "firstname": "Apolo", "lastname": "Lobato Mejia", "age": 1},
]



'''
@ns.route("")
class CatList(Resource):
    @jwt_required # requires "Authorization": "Bearer <token>"
    @ns.doc("list_cats", security='apikey')
    # @ns.marshal_list_with(user, envelope="cats") # Expected response shape (envelope wraps response into an object with the "cats" key)
    def get(self):
        """List all cats"""
        current_user = get_jwt_identity()
        print(current_user)
        return CATS

    @ns.doc("add_new_user")
    @ns.expect(user_register_model, validate=True) # Expected request shape (user_register_model)
    @ns.response(201, "User created successfully", user_wtoken_model)
    @ns.response(409, "User already exists", error_fields)
    # @ns.marshal_with(user_wtoken_model, code=201) # skip_none=True
    # @ns.marshal_with(user, code=201)
    def post(self):
        try:
            args = user_register_parser.parse_args(request) # for input validation
            print(args)
            username = args.get('username') # request.json['username']
            existing_user = User.query.get(username)
            if (existing_user is not None):
                print(f"Error: {existing_user}")
                return throw_exception(USER_REGISTER_EXISTS)
                # return marshal({ 'message': 'User already exists' }, error_fields), 409
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
            }, user_wtoken_model), 201
            # return { 'success': True, 'password': password, 'token': access_token }, 201
        except Exception as error:
            print(error)
            return {"error": True}, 500



@ns.route("/<id>")
@ns.param("id", "The cat identifier")
@ns.response(404, "Cat not found")
class Cat(Resource):
    @ns.doc("get_cat")
    # @ns.marshal_with(user) # Expected response shape
    def get(self, id):
        """Fetch a cat given its identifier"""
        for cat in CATS:
            if cat["id"] == int(id):
                return cat
        ns.abort(404)
    
    @ns.doc('login')
    @ns.expect(user_login_model, validate=True)
    def post(self, id):
        args = user_login_parser.parse_args(request)
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


'''