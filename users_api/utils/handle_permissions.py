import logging
import csv
import sys
from users_db.role_permissions import update_role_permission_table_with_csv


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # set logger level
logFormatter = logging.Formatter("%(levelname)-2s [%(filename)s] %(message)s")
consoleHandler = logging.StreamHandler(sys.stdout)  # set streamhandler to stdout
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


def read_permissions_from_csv(csv_file_path):
    role_permission_list_csv = []
    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            role_permission_list_csv.append(row)
    return role_permission_list_csv


def update_role_permission_records_with_csv(role_permission_csv, logging_on=False):
    results = update_role_permission_table_with_csv(role_permission_csv)

    unchanged_role_permissions = results["unchanged_role_permissions"]
    deleted_role_permissions = results["to_delete_role_permissions"]
    created_role_permissions = results["to_create_role_permissions"]
    # log results
    if logging_on:
        if unchanged_role_permissions:
            logger.info("=====unchanged role_permission records=====")
            for role, permission in unchanged_role_permissions:
                logger.info(f"unchanged_role_permissions: {role} {permission}")
            logger.info("=====unchanged role_permission records=====")

        if deleted_role_permissions:
            logger.info("=====deleted role_permission records=====")
            for role, permission in deleted_role_permissions:
                logger.info(f"to_delete_role_permissions: {role} {permission}")
            logger.info("=====deleted role_permission records=====")

        if created_role_permissions:
            logger.info("=====created role_permission records=====")
            for role, permission in created_role_permissions:
                logger.info(f"to_create_role_permissions: {role} {permission}")
            logger.info("=====created role_permission records=====")
