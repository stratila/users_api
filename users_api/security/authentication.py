import logging
import jwt
import time

from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from users_api.errors.auth import AuthInvalidScheme, AuthInvalidToken, AuthInvalidCode
from users_api.config import settings

from users_db.users import get_user
from users_db.role_permissions import (
    get_permissions_for_role,
)


log = logging.getLogger(__name__)


class JWTToken:
    """JWT token generator and decoder."""

    @staticmethod
    def encode(user_id: int):
        user_role = get_user(user_id)["role"]
        permissions = get_permissions_for_role(user_role)
        permissions = (
            [obj["permission"] for obj in permissions["permissions"]]
            if permissions
            else []
        )

        payload = {
            "user_id": user_id,
            "permissions": permissions,
            # TODO Add refresh tokens to automatically issue new JWTs when they expire.
            "expires": time.time() + settings.access_token_expire_minutes * 60,
        }
        token = jwt.encode(
            payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
        )
        return JWTToken()._token_response(token)

    @staticmethod
    def decode(token: str):
        try:
            decoded_token = jwt.decode(
                token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
            )
            return (
                JWTToken()._token_response(decoded_token)
                if decoded_token["expires"] > time.time()
                else None
            )
        except jwt.PyJWTError as e:
            log.error(f"pyjwt error: {e}")
            return {}

    @staticmethod
    def _token_response(token: str):
        return {"access_token": token}


class JWTBearer(HTTPBearer):
    """A JWT bearer dependency class that validates the JWT token."""

    def __init__(self, auto_error: bool = True):
        self.jwt_token = JWTToken()
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme.lower() == "bearer":
                raise AuthInvalidScheme()
            if not self.validate_jwt(credentials.credentials):
                raise AuthInvalidToken()
            return credentials.credentials
        else:
            raise AuthInvalidCode()

    def validate_jwt(self, token: str) -> bool:
        is_token_valid: bool = False
        payload = self.jwt_token.decode(token=token)
        if payload:
            is_token_valid = True
        return is_token_valid
