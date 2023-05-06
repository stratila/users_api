"""
This file contains the authorization logic for the API.
The authorization logic is based on the permissions that are assigned to a role.
Permissions class dependency:
https://fastapi.tiangolo.com/advanced/advanced-dependencies/
"""
import logging
import re
from fastapi import Depends, HTTPException
from users_api.security.authentication import JWTToken, JWTBearer
from fastapi.requests import Request


logger = logging.getLogger(__name__)


def get_current_user(token: str = Depends(JWTBearer())):
    payload = JWTToken().decode(token)
    if payload:
        # contains the user_id and permissions
        return payload["access_token"]
    return {}


def is_self_write_user(
    request: Request = None, current_user: dict = Depends(get_current_user)
):
    """
    Checks if the current user is trying to update their own record.
    """
    if request:
        path = request.url.path
        method = request.method
        match = re.match(r".*/users/(\d+)", path)
        if match:
            user_id = int(match.group(1))
            if user_id == current_user.get("user_id") and method == "PUT":
                return True
    return False


class Permissions:
    """
    A dependency class that checks if the current user has the required permissions.
    """

    def __init__(self, *args):
        self.permissions_required = set(args)

    def __call__(
        self,
        current_user: dict = Depends(get_current_user),
        self_write_user: bool = Depends(is_self_write_user),
    ):
        return self.check_permissions(
            current_user, self.permissions_required, self_write_user
        )

    def check_permissions(self, current_user, permissions_required, self_write_user):
        permissions = current_user.get("permissions", [])
        # user specific case when updating their own record
        if self_write_user:
            permissions.append("write_users")

        if not set(permissions_required).issubset(set(permissions)):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to perform this action",
            )
        return True
