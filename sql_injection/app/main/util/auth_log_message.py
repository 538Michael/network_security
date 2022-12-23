from flask_restx import Namespace, fields


class AuthLogDTO:
    api = Namespace("auth_log", description="Auth log related operations")

    auth_log_response = api.model(
        "auth_log_response",
        {
            "id": fields.Integer(description="auth log id"),
            "occurred_at": fields.DateTime(description="auth log occurred at"),
            "ip": fields.String(description="auth log ip"),
            "message": fields.String(description="auth log description"),
            "error_code": fields.String(description="auth log error code"),
        },
    )

    auth_log_list = api.model(
        "auth_log_list",
        {
            "current_page": fields.Integer(),
            "total_items": fields.Integer(),
            "total_pages": fields.Integer(),
            "items": fields.List(fields.Nested(auth_log_response)),
        },
    )
