from pydantic import BaseModel, EmailStr, validator
from users_db.schema import Role


class UserBase(BaseModel):
    first_name: str
    middle_name: str | None
    last_name: str
    email: EmailStr
    role: str

    @validator("role")
    def validate_role(cls, v):
        try:
            return Role[v].name
        except KeyError:
            raise ValueError(f"Invalid role. Should be one of {[r.name for r in Role]}")


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    email: EmailStr | None
    role: str | None
    password: str | None


class UserRead(UserBase):
    id: int
