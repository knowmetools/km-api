#!/bin/sh

set -e

MANAGE_PATH=/opt/km-api/km_api/manage.py
MANAGE_CMD="python $MANAGE_PATH"

if [[ "$1" = 'migrate' ]]; then
    ${MANAGE_CMD} migrate
    ${MANAGE_CMD} collectstatic --no-input
    ${MANAGE_CMD} createadmin
    exit 0
fi

if [[ "$1" = 'server' ]]; then
    # First shift to pop 'server' off the arg list. The rest of the arguments
    # are passed as-is to Gunicorn.
    shift
    cd /opt/km-api/km_api
    exec gunicorn km_api.wsgi:application $@
fi

if [[ "$1" = '' ]]; then
    echo "No command provided."
    exit 1
fi

echo "Unrecognized command: $1"
exit 1
