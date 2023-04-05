from pydantic import BaseModel


class UserSignUpSchema(BaseModel):
    first_name: str
    middle_name: str | None
    last_name: str
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "middle_name": "Doe",
                "last_name": "Smith",
                "email": "someemail@gmail.com",
                "password": "password123",
            }
        }


class UserLoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {"email": "someemail@gmail.com", "password": "password123"}
        }
