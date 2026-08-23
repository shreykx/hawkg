from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Any
from utils.db.database import get_db
from utils.quiz import (
    get_quizzes_by_user,
    get_quiz_by_user,
    create_quiz,
    update_quiz,
    delete_quiz,
    QuizQuestionHasResponsesError,
)
from utils.deps import require_auth
from utils.models import Quiz


router = APIRouter(prefix="/quiz", tags=["Quiz"])

class UpdateQuizQuestionRequest(BaseModel):
    id: int | None = None
    prompt: str

class UpdateQuizRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    preferences: dict[str, Any] | None = None
    banner_image: str | None = None
    visibility: str | None = None
    questions: list[UpdateQuizQuestionRequest] | None = None

@router.post("/quizzes")
def create_quiz_route(
    db: Session = Depends(get_db),
    user=Depends(require_auth),
):
    print(">>> CREATE QUIZ ROUTE HIT")
    print(">>> USER:", user.id)

    quiz = create_quiz(
        db=db,
        created_by=user.id,
        title="Untitled Quiz",
    )

    print(">>> CREATED QUIZ:", quiz.id)

    return {"id": quiz.id}


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
    quiz_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_auth),
):
    quiz = get_quiz_by_user(db, quiz_id, user.id)

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return quiz

@router.put("/{quiz_id}")
def update_quiz_route(
    quiz_id: str,
    data: UpdateQuizRequest,
    db: Session = Depends(get_db),
    user=Depends(require_auth),
):
    try:
        quiz = update_quiz(
            db=db,
            quiz_id=quiz_id,
            user_id=user.id,
            title=data.title,
            description=data.description,
            preferences=data.preferences,
            banner_image=data.banner_image,
            visibility=data.visibility,
            questions=[
                {"id": question.id, "prompt": question.prompt}
                for question in data.questions
            ]
            if data.questions is not None
            else None,
        )
    except QuizQuestionHasResponsesError:
        raise HTTPException(
            status_code=409,
            detail="Questions with responses cannot be deleted",
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return {
        "id": quiz.id,
        "questions": [
            {
                "id": question.id,
                "prompt": question.prompt,
                "order_index": question.order_index,
            }
            for question in sorted(quiz.questions, key=lambda question: question.order_index)
        ],
    }

@router.delete("/{quiz_id}")
def delete_quiz_route(
    quiz_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_auth),
):
    quiz = delete_quiz(
        db=db,
        quiz_id=quiz_id,
        user_id=user.id,
    )

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return {"id": quiz.id}
