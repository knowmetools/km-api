#!/bin/sh

set -e

if [ "$1" = 'migrate' ]; then
    exec python /opt/km-api/km_api/manage.py migrate
fi

if [ "$1" = 'server' ]; then
    # First shift to pop 'server' off the arg list. The rest of the arguments
    # are passed as-is to Gunicorn.
    shift
    cd /opt/km-api/km_api
    exec gunicorn km_api.wsgi:application $@
fi

if [ "$1" = '' ]; then
    echo "No command provided."
    exit 1
fi

echo "Unrecognized command: $1"
exit 1
