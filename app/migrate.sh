#!/bin/sh
echo "Running migrate.sh script to run alembic migrations..."

# waiting for postgres server to be ready
python3 postgres_ready.py

# db_users module command that runs alembic upgrade
# to see more detailscheck db_users/commands.py
alembic_upgrade 

echo "Running migrate.sh script done. Exiting..."
