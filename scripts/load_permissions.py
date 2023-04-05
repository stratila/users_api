import pathlib

import users_api
from users_api.utils.read_permissions import read_permissions_from_csv


def load_permissions():
    path = pathlib.Path(users_api.__file__).parent / "security/role_permissions.csv"
    read_permissions_from_csv(path)


def main():
    load_permissions()


if __name__ == "__main__":
    main()
