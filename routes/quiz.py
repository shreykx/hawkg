from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from utils.db.database import get_db
from utils.quiz import get_quizzes_by_user

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.get("/quizzes")
def get_quizzes(
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")

    if not user_id:
        return {"error": "Not authenticated"}

    return get_quizzes_by_user(db, user_id)