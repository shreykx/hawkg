from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime,
    UniqueConstraint, JSON, func, CheckConstraint
)
from sqlalchemy.orm import relationship
from utils.db.database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    preferences = Column(JSON, nullable=False, default=dict) 
    banner_image = Column(String, nullable=True)
    submissions = relationship("QuizSubmission", back_populates="quiz", cascade="all, delete-orphan")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")


class QuizSubmission(Base):
    """One row per user per quiz — the atomic 'did they submit' gate."""
    __tablename__ = "quiz_submissions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    quiz = relationship("Quiz", back_populates="submissions")
    responses = relationship("Response", back_populates="submission", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("quiz_id", "user_id", name="uq_quiz_submission"),
    )

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    prompt = Column(Text, nullable=False)
    question_type = Column(String, nullable=False)  # e.g. "mcq", "free_text"
    order_index = Column(Integer, nullable=False, default=0)
    options = Column(JSON, nullable=True)  # for mcq-type questions
    preferences = Column(JSON, nullable=False, default=dict)  # per-question overrides

    quiz = relationship("Quiz", back_populates="questions")
    responses = relationship("Response", back_populates="question", cascade="all, delete-orphan")

class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    submission_id = Column(Integer, ForeignKey("quiz_submissions.id"), nullable=False)
    answer = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    question = relationship("QuizQuestion", back_populates="responses")
    submission = relationship("QuizSubmission", back_populates="responses")

    __table_args__ = (
        UniqueConstraint("question_id", "submission_id", name="uq_response_per_submission"),
    )


class Digest(Base):
    """Pseudonymous AI-generated summary of free-text responses, per question."""
    __tablename__ = "digests"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False, unique=True)
    summary = Column(Text, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    source_response_count = Column(Integer, nullable=False, default=0)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=True)
    google_id = Column(String, unique=True, nullable=True, index=True)
    profile_image = Column(String, nullable=True)
    profile_image_version = Column(Integer, default=1)
    display_name = Column(String, nullable=True)
    role = Column(String, default="user", nullable=False)

    __table_args__ = (
        CheckConstraint(
            "password_hash IS NOT NULL OR google_id IS NOT NULL",
            name="user_has_auth_method",
        ),
    )