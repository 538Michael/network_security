from sqlalchemy import func

from .. import db


class SQLInjectionDetectionLog(db.Model):
    __tablename__ = "sql_injection_detection_log"

    id = db.Column(db.Integer, primary_key=True)
    occurred_at = db.Column(db.DateTime, server_default=func.now())
    error_code = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"<SQLInjectionDetectionLog {self.message}>"
