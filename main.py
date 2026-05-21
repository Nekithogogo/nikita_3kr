from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse
import secrets

from config import settings
from database import init_db
from rate_limit import init_limiter
from auth import fake_users_db
from security import get_password_hash
from models import UserInDB

import auth_router
import rbac_router
import sqlite_router
import todos_router

app = FastAPI(
    title="FastAPI Control Work #3",
    description="Реализация аутентификации, JWT, RBAC, SQLite CRUD",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

init_limiter(app)
init_db()

app.include_router(auth_router.router)
app.include_router(rbac_router.router)
app.include_router(sqlite_router.router)
app.include_router(todos_router.router)

def check_docs_auth(credentials: HTTPBasicCredentials = Depends(HTTPBasic(auto_error=False))):
    if settings.MODE == "PROD":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    elif settings.MODE == "DEV":
        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Basic"},
            )
        if not (secrets.compare_digest(credentials.username, settings.DOCS_USER) and
                secrets.compare_digest(credentials.password, settings.DOCS_PASSWORD)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        return True
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

if settings.MODE == "DEV":
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html(auth: bool = Depends(check_docs_auth)):
        return get_swagger_ui_html(openapi_url="/openapi.json", title="API Docs")

    @app.get("/openapi.json", include_in_schema=False)
    async def custom_openapi(auth: bool = Depends(check_docs_auth)):
        return JSONResponse(content=get_openapi(title=app.title, version=app.version, routes=app.routes))
else:
    @app.get("/docs", include_in_schema=False)
    @app.get("/openapi.json", include_in_schema=False)
    @app.get("/redoc", include_in_schema=False)
    async def docs_404():
        return JSONResponse(status_code=404, content={"detail": "Not Found"})

@app.get("/")
async def root():
    return {"message": "FastAPI Control Work #3", "mode": settings.MODE}