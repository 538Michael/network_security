from flask import request
from flask_restx import Resource

from ..config import Config
from ..service import get_users, save_new_user
from ..util import DefaultResponsesDTO, UserDTO

user_ns = UserDTO.api
api = user_ns
_user_post = UserDTO.user_post
_user_list = UserDTO.user_list
_user_response = UserDTO.user_response

_default_message_response = DefaultResponsesDTO.message_response

_CONTENT_PER_PAGE = Config.CONTENT_PER_PAGE
_DEFAULT_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


@api.route("")
class User(Resource):
    @api.doc(
        "list_of_registered_users",
        params={
            "page": {"description": "Page number", "default": "1", "type": "int"},
            "per_page": {
                "description": "Items per page",
                "default": _DEFAULT_CONTENT_PER_PAGE,
                "enum": _CONTENT_PER_PAGE,
                "type": int
            },
            "username": {"description": "User username", "type": str},
        },
        description=f"List of registered users with pagination. {_DEFAULT_CONTENT_PER_PAGE} users per page.",
    )
    @api.marshal_with(_user_list, code=200, description="users_list ")
    def get(self):
        """List all registered users"""
        params = request.args
        return get_users(params=params)

    @api.doc("create a new user")
    @api.expect(_user_post, validate=True)
    @api.response(201, "user_created", _default_message_response)
    @api.response(409, "username_in_use", _default_message_response)
    def post(self) -> tuple[dict[str, str], int]:
        """Creates a new user"""
        data = request.json
        save_new_user(data=data)
        return {"message": "user_created"}, 201
