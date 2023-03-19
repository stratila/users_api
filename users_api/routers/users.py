from fastapi import APIRouter, Query
from users_api.schemas.users import UserCreate, UserRead, UserUpdate
from users_api.errors.users import UserNotFound

from users_db.users import (
    create_user,
    get_user,
    get_users,
    update_user,
    delete_user,
)

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=201)
def user_post(user: UserCreate):
    user_id = create_user(**user.dict())
    return {"id": user_id, **user.dict()}


@router.get("/{user_id}", response_model=UserRead)
def user_get(user_id: int):
    user = get_user(user_id)
    if not user:
        raise UserNotFound(user_id)
    return user


@router.get("/", response_model=list[UserRead])
def users_get(
    user_id: int | None = Query(default=None),
    user_ids: list[int] | None = Query(default=None),
    first_name: str | None = Query(default=None),
    middle_name: str | None = Query(default=None),
    last_name: str | None = Query(default=None),
):
    users = get_users(user_id, user_ids, first_name, middle_name, last_name)
    return users


@router.put("/{user_id}", response_model=UserRead)
def user_put(user_id: int, user: UserUpdate):
    updated_record_id = update_user(user_id, **user.dict())
    if not updated_record_id:
        raise UserNotFound(user_id)
    return {"id": user_id, **user.dict()}


@router.delete("/{user_id}", status_code=204)
def user_delete(user_id: int):
    delete_user(user_id)
