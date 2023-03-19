import logging

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from routers import users

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


app.include_router(users.router, prefix="/users", tags=["users"])
