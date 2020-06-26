from flask_restx import fields, reqparse

from app import api


def append_error_fields(ns):
	return ns.model("error_fields", {
		"message": fields.String(required=False, description="Error message"),
	})