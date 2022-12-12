from app.main import db
from app.main.model import (
    User,
)


def create_seed():
    _add_user()
    db.session.commit()


def _add_user():
    new_user = User(
        username="admin",
        password="admin123",
    )

    db.session.add(new_user)
    db.session.flush()
