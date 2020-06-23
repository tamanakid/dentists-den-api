# expect a token somewhere: 
# When sending a request with swagger, it will automatically send the given "Authorization header"

'''
autho = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(..., authorizations=autho, ...)
'''

# Add to each endpoint to tell swagger that it requires authorization
# (THIS DOESN'T CHANGE THE API FUNCTIONS, ONLY THE SWAGGER INTERFACE)
''' @api.doc(..., security='apikey') '''


# We add the "Token decorator", which will be used by the class methods' endpoints like so:
'''
@ns.doc
@ns.token_required
'''

from flask import request
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return { 'message': 'Token missing' }, 401
        print(f'Token: {token}')
        return f(*args, **kwargs)
    return decorated