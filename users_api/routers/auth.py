from fastapi import APIRouter
from users_api.security.password import (
    check_password_hash,
    get_password_hash,
)
from users_api.security.authentication import (
    JWTToken
)
from users_api.schemas.auth import (
    UserLoginSchema,
    UserSignUpSchema,
)
from users_api.errors.auth import (
    AuthWrongCredentials,
)
from users_db.users import (
    create_user,
    get_hashed_password_by_email,
)
from users_db.users import ROLE_USER

router = APIRouter()


@router.post("/signup")
async def signup(user: UserSignUpSchema):
    user = user.dict()
    user["password"] = get_password_hash(user["password"])
    user["role"] = ROLE_USER
    user_id = create_user(**user)  # TODO handle user already exists
    return JWTToken().encode(user_id)


@router.post("/login")
async def login(user: UserLoginSchema):
    payload = user.dict()
    user = get_hashed_password_by_email(payload["email"])
    if user and check_password_hash(payload["password"], user["hashed_password"]):
        return JWTToken().encode(user["id"])
    raise AuthWrongCredentials()
