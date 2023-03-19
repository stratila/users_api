from pydantic import BaseModel


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
