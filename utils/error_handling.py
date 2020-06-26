from flask_restx import fields, reqparse, marshal

from app import api
from .exceptions_global import exceptions_global, GLOBAL_SERVER_ERROR



# Call at each module's models_api to define the "error_fields" model within its namespace
def append_error_fields(ns):
	return ns.model("error_fields", {
		"message": fields.String(required=False, description="Error message"),
	})



# Call at each module's exceptions to define the "throw_exception" function with its local exceptions
def append_throw_exception(exceptions_mod, error_fields):

	def throw_exception(cod):
		print(f"ExceptionCod: {cod}")

		if (cod in exceptions_global):
			exc = exceptions_global[cod]
		elif (cod in exceptions_mod):
			exc = exceptions_mod[cod]
		else:
			print(f"{cod} not found in module or global exceptions")
			exc = GLOBAL_SERVER_ERROR

		print(f"Exception: {cod} ({exc['marshal']['message']})")

		return marshal(exc['marshal'], error_fields), exc['status_code']
	
	return throw_exception