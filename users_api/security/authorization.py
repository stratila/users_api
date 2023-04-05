"""
This file contains the authorization logic for the API.
The authorization logic is based on the permissions that are assigned to a role.
Permissions class dependency:
https://fastapi.tiangolo.com/advanced/advanced-dependencies/
"""
import logging
from fastapi import Depends, HTTPException
from users_api.security.authentication import JWTToken, JWTBearer


logger = logging.getLogger(__name__)


def get_current_user(token: str = Depends(JWTBearer())):
    payload = JWTToken().decode(token)
    if payload:
        # contains the user_id and permissions
        return payload["access_token"]
    return {}


class Permissions:
    """
    A dependency class that checks if the current user has the required permissions.
    """

    def __init__(self, *args):
        self.permissions_required = set(args)

    def __call__(self, current_user: dict = Depends(get_current_user)):
        return self.check_permissions(current_user, self.permissions_required)

    def check_permissions(self, current_user, permissions_required):
        permissions = current_user.get("permissions", [])
        if not set(permissions_required).issubset(set(permissions)):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to perform this action",
            )
        return True
