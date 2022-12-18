from app.main import db
from ..model import SQLInjectionDetectionLog


def add_sql_injection_detection_log_message(ip: str, message: str, error_code: str = None) -> None:
    new_sql_injection_detection_log = SQLInjectionDetectionLog(ip=ip, error_code=error_code, message=message)

    save_changes(new_sql_injection_detection_log)


def save_changes(data: SQLInjectionDetectionLog) -> None:
    db.session.add(data)
    db.session.commit()
