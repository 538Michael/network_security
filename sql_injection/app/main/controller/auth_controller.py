from flask import request
from flask_restx import Resource

from app.main.service.auth_service import login
from app.main.util.auth_dto import AuthDTO
from ..util import DefaultResponsesDTO

auth_ns = AuthDTO.api
api = auth_ns
_auth = AuthDTO.auth

_default_message_response = DefaultResponsesDTO.message_response


@api.route("")
class Login(Resource):
    @api.doc("User login")
    @api.expect(_auth, validate=True)
    @api.response(401, "incorrect_information", _default_message_response)
    def post(self):
        """User login"""
        data = request.json
        login(ip=request.remote_addr, data=data)
        return {"message": "login_successfully"}, 200
