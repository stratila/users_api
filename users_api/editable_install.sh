#!/bin/sh

# install users_db as editable, it allows to edit the code without rebuilding the image
# because the code is mounted as a volume in docker-compose file.

if [ -d /users_db ]
    then pip install -e /users_db
fi;
