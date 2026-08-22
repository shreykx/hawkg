from fastapi import FastAPI, Request, Depends
import uvicorn

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from utils.db.database import Base, engine
from utils import models
from utils.deps import require_auth, NotAuthenticated

from routes.auth import router as auth_router
from routes.quiz import router as quiz_router

from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(quiz_router)

templates = Jinja2Templates(directory="templates")


@app.exception_handler(NotAuthenticated)
async def not_authenticated_handler(request: Request, exc: NotAuthenticated):
    return RedirectResponse("/auth?mode=signin", status_code=303)


@app.get("/")
async def landing(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="landing.html",
    )


@app.get("/auth")
async def auth(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="auth/auth.html",
    )


@app.get("/dashboard")
async def dashboard(
    request: Request,
    user=Depends(require_auth),
):
    return templates.TemplateResponse(
        request=request,
        name="protected/dashboard.html",
        context={"user": user},
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )