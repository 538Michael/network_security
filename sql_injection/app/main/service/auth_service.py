from typing import Dict

from sqlalchemy.sql.expression import text

from .sql_injection_detection_log_service import add_sql_injection_detection_log_message
from ..exceptions import DefaultException
from ..model import User


def login(data: Dict[str, any]) -> str:
    username = data.get("username")
    password = data.get("password")

    filters = [text("username='{}'".format(username)), text("password='{}'".format(password))]

    try:
        user = User.query.filter(*filters).scalar()
    except Exception as e:
        print(e)

    if not user:
        raise DefaultException(message="incorrect_information", code=401)

    filters = [User.username == username, User.password == password]

    try:
        user = User.query.filter(*filters).scalar()
    except Exception as e:
        print(e)

    if not user:
        add_sql_injection_detection_log_message(error_code=18456, message="Login failed for user {}".format(username))

    return "login_successfully"
