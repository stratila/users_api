import pathlib

import users_api
from users_api.utils.handle_permissions import (
    read_permissions_from_csv,
    update_role_permission_records_with_csv,
)


def load_permissions():
    """Updates the role_permission table with the role_permissions.csv file."""
    path = pathlib.Path(users_api.__file__).parent / "security/role_permissions.csv"
    role_permissions_csv_list = read_permissions_from_csv(path)
    update_role_permission_records_with_csv(role_permissions_csv_list, logging_on=True)


def main():
    load_permissions()


if __name__ == "__main__":
    main()
