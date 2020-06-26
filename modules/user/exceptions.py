from utils.error_handling import append_throw_exception
from .models_api import error_fields



exceptions = {
	'USER_REGISTER_EXISTS': {
		'marshal': { 'message': 'User already exists' },
		'status_code': 409
	}
}


USER_REGISTER_EXISTS = 'USER_REGISTER_EXISTS'


# Module exception handler
throw_exception = append_throw_exception(exceptions, error_fields)