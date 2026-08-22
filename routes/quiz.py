from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from utils.db.database import get_db
from utils.quiz import get_quizzes_by_user, get_quiz_by_user
from utils.deps import require_auth

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


@router.get("/{quiz_id}")
def get_quiz_route(
    quiz_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_auth),
):
    quiz = get_quiz_by_user(db, quiz_id, user.id)

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return quiz