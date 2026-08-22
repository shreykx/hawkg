from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

from utils.models import Quiz, QuizSubmission, QuizQuestion


def get_quizzes_by_user(db: Session, user_id: str):
    submission_counts = (
        db.query(
            QuizSubmission.quiz_id,
            func.count(QuizSubmission.id).label("submission_count"),
        )
        .group_by(QuizSubmission.quiz_id)
        .subquery()
    )

    question_counts = (
        db.query(
            QuizQuestion.quiz_id,
            func.count(QuizQuestion.id).label("question_count"),
        )
        .group_by(QuizQuestion.quiz_id)
        .subquery()
    )

    rows = (
        db.query(
            Quiz,
            func.coalesce(submission_counts.c.submission_count, 0).label(
                "submission_count"
            ),
            func.coalesce(question_counts.c.question_count, 0).label("question_count"),
        )
        .outerjoin(submission_counts, Quiz.id == submission_counts.c.quiz_id)
        .outerjoin(question_counts, Quiz.id == question_counts.c.quiz_id)
        .filter(Quiz.created_by == user_id)
        .all()
    )

    return [
        {
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "banner_image": quiz.banner_image,
            "created_at": quiz.created_at,
            "updated_at": quiz.updated_at,
            "total_submissions": submission_count,
            "total_questions": question_count,
        }
        for quiz, submission_count, question_count in rows
    ]


def get_quiz(db: Session, quiz_id: int):
    quiz = (
        db.query(Quiz)
        .options(selectinload(Quiz.questions))
        .filter(Quiz.id == quiz_id)
        .first()
    )

    if not quiz or quiz.visibility != "public":
        return None

    return {
        "id": quiz.id,
        "created_at": quiz.created_at,
        "title": quiz.title,
        "description": quiz.description,
        "created_by": quiz.created_by,
        "banner_image": quiz.banner_image,
        "questions": [
            {
                "id": q.id,
                "prompt": q.prompt,
                "question_type": q.question_type,
                "order_index": q.order_index,
                "options": q.options,
                "preferences": q.preferences,
            }
            for q in sorted(quiz.questions, key=lambda q: q.order_index)
        ],
    }

def create_quiz(
    db: Session,
    created_by: int,
    title: str,
    description: str | None = None,
    preferences: dict | None = None,
    banner_image: str | None = None,
    visibility: str = "unlisted",
):
    quiz = Quiz(
        title=title,
        description=description,
        created_by=created_by,
        preferences=preferences or {},
        banner_image=banner_image,
        visibility=visibility,
    )

    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    return quiz