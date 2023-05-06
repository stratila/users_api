import logging
import pkg_resources

from fastapi import FastAPI, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from users_api.routers import auth, users
from users_api.security.authentication import JWTBearer
from users_api.config import settings

from users_db.errors import DatabaseError

logger = logging.getLogger(__name__)


app = FastAPI()


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            {"code": 500, "error_message": "Internal Server Error"}
        ),
    )


@app.exception_handler(DatabaseError)
async def database_exception_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"code": 400, "error_message": str(exc)}),
    )


resources = ["*"]
if settings.cors_origins:
    resources = settings.cors_origins.split(",")
else:
    logger.warning(
        "No CORS origins specified. This is not recommended for "
        "production environments."
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=resources,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(
    users.router, prefix="/users", tags=["users"], dependencies=[Depends(JWTBearer())]
)


@app.get("/")
async def info():
    return {
        "app": "Users API",
        "versions": {
            "users_api": pkg_resources.get_distribution("users-api").version,
            "users_db": pkg_resources.get_distribution("users-db").version,
        },
    }
