# docker compose up  --build --force-recreate --no-deps

from flask_restx import Api

from .main.controller import (
    user_ns,
    auth_ns,
    auth_log_ns
)
from .main.exceptions import DefaultException, ValidationException
from .main.util import DefaultResponsesDTO

authorizations = {
    "api_key": {"type": "apiKey", "in": "header", "name": "Authorization"}
}

api = Api(
    authorizations=authorizations,
    title="Network Security",
    version="1.0",
    description="SQL Injection",
    security="apikey",
)

api.add_namespace(user_ns, path="/user")
api.add_namespace(auth_ns, path="/auth")
api.add_namespace(auth_log_ns, path="/auth_log")

api.add_namespace(DefaultResponsesDTO.api)

# Exception Handler
api.errorhandler(DefaultException)


@api.errorhandler(ValidationException)
def handle_validation_exception(error):
    """Return a list of errors and a message"""
    return {"errors": error.errors, "message": error.message}, error.code
