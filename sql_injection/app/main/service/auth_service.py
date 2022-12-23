import re
from typing import Dict

import sqlalchemy.exc
from sqlalchemy.sql.expression import text

from app.main import db
from .auth_log_service import add_auth_log_message
from ..exceptions import DefaultException
from ..model import User

detect_using_regex = True
regexes_to_test = [';\s*(SELECT)\s*.*FROM\s*.*WHERE\s*.*',
                   ';\s*(INSERT)\s*.*INTO\s*.*VALUES\s*.*',
                   ';\s*(UPDATE)\s*.*SET\s*.*',
                   ';\s*(DELETE)\s*FROM\s*.*']


def regex_check(ip: str, strings: list):
    for string in strings:
        for expression in regexes_to_test:
            regex = re.search(expression, string, re.IGNORECASE)

            if regex:
                add_auth_log_message(ip=ip,
                                     message="SQL Injection detected using {}.".format(
                                         regex.group(1).upper()))
                raise DefaultException("sql_injection_detected", code=200)


def login(ip: str, data: Dict[str, any]) -> str:
    username = data.get("username")
    password = data.get("password")

    if detect_using_regex:
        regex_check(ip=ip, strings=[username, password])
    filters = [text("username='{}'".format(username)), text("password='{}'".format(password))]

    try:
        # SELECT *
        # FROM "user"
        # WHERE username='admin' AND password='admin123'
        user = User.query.filter(*filters).scalar()
    except sqlalchemy.exc.DBAPIError as e:
        db.session.rollback()
        if e.args and e.args[0]:
            error_msg = e.args[0].split('\n')[0]
            error_msg = error_msg[error_msg.find(')') + 2:].capitalize()
        add_auth_log_message(ip=ip, message="{}.".format(error_msg),
                             error_code=e.orig.pgcode)
        raise DefaultException("incorrect_information", code=401)

    if not user:
        add_auth_log_message(ip=ip,
                             message="Login failed for user '{}'.".format(
                                 username), error_code=18456)
        raise DefaultException(message="incorrect_information", code=401)
    elif user.username != username:
        add_auth_log_message(ip=ip, message="Login failed for user '{}'.".format(
            username), error_code=18456)
        raise DefaultException(message="incorrect_information", code=401)

    filters = [User.username == username]

    # SELECT *
    # FROM "user"
    # WHERE "user".username = %(username_1)s
    # {'username_1': 'admin'}
    user = User.query.filter(*filters).scalar()

    if user and user.password != password:
        add_auth_log_message(ip=ip, message="SQL Injection detected. Password: {}".format(password))
        raise DefaultException("sql_injection_detected", code=200)

    return "login_successfully"
