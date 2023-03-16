import logging

from pydantic import BaseModel
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from users_db.users import (
    create_user,
    get_user,
    get_users,
    update_user,
    delete_user,
)

# TODO refactor to use separate files

logger = logging.getLogger(__name__)


class UserNotFound(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=404, detail=f"User with id {user_id} not found")


class UserError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=400, detail=message)


class UserBase(BaseModel):
    first_name: str
    middle_name: str | None
    last_name: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: int


app = FastAPI()


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            {"code": 500, "error_message": "Internal Server Error"}
        ),
    )


@app.post("/users", response_model=UserRead, status_code=201)
def user_post(user: UserCreate):
    user_id = create_user(**user.dict())
    return {"id": user_id, **user.dict()}


@app.get("/users/{user_id}", response_model=UserRead)
def user_get(user_id: int):
    user = get_user(user_id)
    if not user:
        raise UserNotFound(user_id)
    return user


@app.get("/users/", response_model=list[UserRead])
def users_get(
    user_id: int | None = Query(default=None),
    user_ids: list[int] | None = Query(default=None),
    first_name: str | None = Query(default=None),
    middle_name: str | None = Query(default=None),
    last_name: str | None = Query(default=None),
):
    users = get_users(user_id, user_ids, first_name, middle_name, last_name)
    return users


@app.put("/users/{user_id}", response_model=UserRead)
def user_put(user_id: int, user: UserUpdate):
    updated_record_id = update_user(user_id, **user.dict())
    if not updated_record_id:
        raise UserNotFound(user_id)
    return {"id": user_id, **user.dict()}


@app.delete("/users/{user_id}", status_code=204)
def user_delete(user_id: int):
    delete_user(user_id)
