from fastapi import HTTPException


class UserNotFound(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=404, detail=f"User with id {user_id} not found")


class UserError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=400, detail=message)
