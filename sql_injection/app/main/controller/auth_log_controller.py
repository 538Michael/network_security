from flask import request
from flask_restx import Resource

from ..config import Config
from ..service import get_auth_logs
from ..util import DefaultResponsesDTO, AuthLogDTO

auth_log_ns = AuthLogDTO.api
api = auth_log_ns
_auth_log_list = AuthLogDTO.auth_log_list
_auth_log_response = AuthLogDTO.auth_log_response

_default_response = DefaultResponsesDTO.message_response

_CONTENT_PER_PAGE = Config.CONTENT_PER_PAGE
_DEFAULT_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


@api.route("")
class AuthLog(Resource):
    @api.doc(
        "list_of_registered_auth_logs",
        params={
            "page": {"description": "Page number", "default": "1", "type": "int"},
            "per_page": {
                "description": "Items per page",
                "default": _DEFAULT_CONTENT_PER_PAGE,
                "enum": _CONTENT_PER_PAGE,
                "type": int
            },
            "auth_log_description": {"description": "Auth log  description", "type": str},
        },
        description=f"List of registered auth log s with pagination. {_DEFAULT_CONTENT_PER_PAGE} auth log s per page.",
    )
    @api.marshal_with(_auth_log_list, code=200, description="auth_log_s_list ")
    def get(self):
        """List all registered auth logs"""
        params = request.args
        return get_auth_logs(params=params)
