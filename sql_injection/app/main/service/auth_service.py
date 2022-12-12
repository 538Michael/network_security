from typing import Dict

import bcrypt

from ..exceptions import DefaultException
from ..model import User


def check_password(password_one: str, password_two: str) -> bool:
    password_one = password_one.encode("utf-8")
    password_two = password_two.encode("utf-8")
    return bcrypt.checkpw(password_one, password_two)


def login(data: Dict[str, any]) -> str:
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).scalar()

    if not user:
        raise DefaultException(message="incorrect_information", code=401)

    user_password = user.password

    if not check_password(password, user_password):
        raise DefaultException("incorrect_information", code=401)

    return "login_successfully"
