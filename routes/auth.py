from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse

from utils.db.database import SessionLocal
from utils.models import User
from utils.auth import hash_password, verify_password

import os

from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


router = APIRouter(prefix="/auth")


@router.post("/signup")
async def signup(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    display_name: str = Form(...),
    password: str = Form(...),
):
    db = SessionLocal()
    try:
        existing_user = (
            db.query(User)
            .filter((User.email == email) | (User.username == username))
            .first()
        )
        if existing_user:
            return RedirectResponse(
                "/auth?mode=signup&error=user_exists", status_code=303
            )
        user = User(
            email=email, username=username, display_name=display_name or username, password_hash=hash_password(password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        request.session["user_id"] = user.id

        return RedirectResponse("/dashboard", status_code=303)
    finally:
        db.close()


@router.post("/signin")
async def signin(request: Request, email: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user or not user.password_hash:
            return RedirectResponse(
                "/auth?mode=signin&error=invalid_credentials", status_code=303
            )
        if not verify_password(password, user.password_hash):
            return RedirectResponse(
                "/auth?mode=signin&error=invalid_credentials", status_code=303
            )
        request.session["user_id"] = user.id

        return RedirectResponse("/dashboard", status_code=303)
    finally:
        db.close()


@router.post("/signout")
async def signout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


@router.get("/google")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)

    userinfo = token["userinfo"]

    google_id = userinfo["sub"]
    email = userinfo["email"]
    profile_image = userinfo.get("picture")

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.google_id == google_id).first()

        if not user:
            user = db.query(User).filter(User.email == email).first()

        if not user:
            user = User(
                email=email,
                username=email.split("@")[0],
                google_id=google_id,
                profile_image=profile_image,
                display_name=userinfo.get("name")
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        else:
            if not user.google_id:
                user.google_id = google_id
            if profile_image:
                user.profile_image = profile_image
            if not user.display_name:
                user.display_name = userinfo.get("name")
            db.commit()

        request.session["user_id"] = user.id

        return RedirectResponse("/dashboard", status_code=303)

    finally:
        db.close()