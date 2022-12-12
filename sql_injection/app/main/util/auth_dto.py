from flask_restx import Namespace, fields


class AuthDTO:
    api = Namespace("auth", description="Authentication related operations")

    auth = api.model(
        "login",
        {
            "username": fields.String(
                required=True, description="user username", max_length=128
            ),
            "password": fields.String(
                required=True, description="user password", min_length=8, max_length=128
            ),
        },
    )
