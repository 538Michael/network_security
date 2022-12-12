from app.main import db
from app.main.model import (
    User,
)
from app.main.service import hash_password


def create_seed():
    _add_user()
    db.session.commit()


def _add_user():
    new_user = User(
        username="admin",
        password=hash_password("admin123"),
    )

    db.session.add(new_user)
    db.session.flush()
