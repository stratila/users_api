from users_db.users import get_user
from users_db.role_permissions import ROLE_SUPER_ADMIN, ROLE_ADMIN, ROLE_USER
from users_api.errors.users import UserNotFound, UserError


def check_role_updates(user_id: int, current_user: dict):
    # cannot update own role
    if user_id == current_user["user_id"]:
        raise UserError("Cannot update own role")
    # get full user object
    current_user = get_user(current_user["user_id"])
    update_user = get_user(user_id)
    if not update_user:
        raise UserNotFound(user_id)

    current_user_role = current_user["role"]
    update_user_role = update_user["role"]

    if current_user_role == ROLE_SUPER_ADMIN:
        if update_user_role == ROLE_SUPER_ADMIN:
            raise UserError("Cannot update super admin role")
    if current_user_role == ROLE_ADMIN:
        if update_user_role == ROLE_SUPER_ADMIN:
            raise UserError("Cannot update super admin role")
        if update_user_role == ROLE_ADMIN:
            raise UserError("Cannot update admin role")
    if current_user_role == ROLE_USER:
        if update_user_role == ROLE_SUPER_ADMIN:
            raise UserError("Cannot update super admin role")
        if update_user_role == ROLE_ADMIN:
            raise UserError("Cannot update admin role")
        if update_user_role == ROLE_USER:
            raise UserError("Cannot update user role")
