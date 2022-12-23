from sqlalchemy import func

from .. import db


class AuthLog(db.Model):
    __tablename__ = "auth_log"

    id = db.Column(db.Integer, primary_key=True)
    occurred_at = db.Column(db.DateTime, server_default=func.now())
    ip = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    error_code = db.Column(db.String)

    def __repr__(self) -> str:
        return f"<AuthLog {self.message}>"
