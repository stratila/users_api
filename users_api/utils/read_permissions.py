import csv
from users_db.role_permissions import (
    delete_role_permissions,
    create_permission_for_role,
)
from users_db.role_permissions import Role


def read_permissions_from_csv(csv_file_path):
    # clean up existing permissions
    for role in Role:
        delete_role_permissions(role.name)

    # read permissions from CSV file
    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # FIXME: In future it will raise an exception if (role,permission) pair is
            # already present
            create_permission_for_role(row["role"], row["permission"])
            # TODO: make more intelligent way to handle missing permissions from csv
            # i.e delete permissions from db if not present in csv
