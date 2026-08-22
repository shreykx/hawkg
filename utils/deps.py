# utils/dependencies.py

from fastapi import Request
from utils.db.database import SessionLocal
from utils import models


class NotAuthenticated(Exception):
    pass


def require_auth(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        raise NotAuthenticated()

    db = SessionLocal()

    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()

        if not user:
            request.session.clear()
            raise NotAuthenticated()

        db.expunge(user)
        return user

    finally:
        db.close()