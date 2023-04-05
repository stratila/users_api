import logging

from fastapi import APIRouter, Query, Depends

from users_api.security.authorization import Permissions
from users_api.security.password import get_password_hash
from users_api.schemas.users import UserCreate, UserRead, UserUpdate
from users_api.errors.users import UserNotFound

from users_db.users import (
    create_user,
    get_user,
    get_users,
    update_user,
    delete_user,
)

log = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/",
    response_model=UserRead,
    status_code=201,
    dependencies=[Depends(Permissions("write_users"))],
)
def user_post(user: UserCreate):
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user_dict["password"])
    user_id = create_user(**user_dict)
    return {"id": user_id, **user_dict}


@router.get(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(Permissions("read_users"))],
)
def user_get(user_id: int):
    user = get_user(user_id)
    if not user:
        raise UserNotFound(user_id)
    return user


@router.get(
    "/",
    response_model=list[UserRead],
    dependencies=[Depends(Permissions("read_users"))],
)
def users_get(
    user_id: int | None = Query(default=None),
    user_ids: list[int] | None = Query(default=None),
    first_name: str | None = Query(default=None),
    middle_name: str | None = Query(default=None),
    last_name: str | None = Query(default=None),
    role: str | None = Query(default=None),
    email: str | None = Query(default=None),
):
    users = get_users(
        user_id, user_ids, first_name, middle_name, last_name, email, role
    )
    return users


@router.put(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(Permissions("write_users"))],
)
def user_put(user_id: int, user: UserUpdate):
    # remove None values from user dict
    user_dict = {k: v for k, v in user.dict().items() if v is not None}

    # hash password if it is in the user dict
    if "password" in user_dict:
        user_dict["password"] = get_password_hash(user_dict["password"])

    updated_user = update_user(
        user_id,
        **user_dict,
    )

    if not updated_user:
        raise UserNotFound(user_id)
    return updated_user


@router.delete(
    "/{user_id}", status_code=204, dependencies=[Depends(Permissions("write_users"))]
)
def user_delete(user_id: int):
    delete_user(user_id)
