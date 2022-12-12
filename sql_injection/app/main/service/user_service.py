import math

import bcrypt
from werkzeug.datastructures import ImmutableMultiDict

from .. import db
from ..config import Config
from ..exceptions import DefaultException
from ..model import User

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def get_users(params: ImmutableMultiDict):
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    username = params.get("username", type=str)

    filters = []

    if username:
        filters.append(User.username.ilike(f"%{username}%"))

    pagination = (
        User.query.filter(*filters)
        .order_by(User.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    total, users = pagination.total, pagination.items

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": math.ceil(total / _CONTENT_PER_PAGE),
        "items": users,
    }


def save_new_user(data: dict[str, str]) -> None:
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).scalar()

    if user:
        raise DefaultException("username_in_use", code=409)

    password = hash_password(password)

    new_user = User(
        username=username,
        password=password,
    )

    save_changes(new_user)


def save_changes(data: User) -> None:
    db.session.add(data)
    db.session.commit()


def hash_password(password: str) -> str:
    password = password.encode("utf-8")
    return bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
