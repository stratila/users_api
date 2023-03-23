#!/bin/sh

set -e  # exit on error
echo "migrate.sh: run alembic migrations..."
python3 -u /scripts/postgres_is_ready.py  # waiting for postgres server to be ready
alembic_upgrade  # db_users module command that runs alembic upgrade
echo "migrate.sh: migrations done |✓|"
