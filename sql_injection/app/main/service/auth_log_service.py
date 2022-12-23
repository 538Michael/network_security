import math

from werkzeug.datastructures import ImmutableMultiDict

from app.main import db
from ..config import Config
from ..model import AuthLog

_CONTENT_PER_PAGE = Config.DEFAULT_CONTENT_PER_PAGE


def add_auth_log_message(ip: str, message: str, error_code: str = None) -> None:
    new_auth_log_message = AuthLog(ip=ip, error_code=error_code, message=message)

    save_changes(new_auth_log_message)


def get_auth_logs(params: ImmutableMultiDict):
    page = params.get("page", type=int, default=1)
    per_page = params.get("per_page", type=int, default=_CONTENT_PER_PAGE)
    username = params.get("username", type=str)

    filters = []

    if username:
        filters.append(AuthLog.username.ilike(f"%{username}%"))

    pagination = (
        AuthLog.query.filter(*filters)
        .order_by(AuthLog.id)
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    total, auth_logs = pagination.total, pagination.items

    return {
        "current_page": page,
        "total_items": pagination.total,
        "total_pages": math.ceil(total / _CONTENT_PER_PAGE),
        "items": auth_logs,
    }


def save_changes(data: AuthLog) -> None:
    db.session.add(data)
    db.session.commit()
