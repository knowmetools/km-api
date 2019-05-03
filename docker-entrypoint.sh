#!/bin/sh

set -euf

MANAGE_PATH=/opt/km-api/km_api/manage.py
MANAGE_CMD="python $MANAGE_PATH"

# Get sentry to generate a release version based on the current commit
# hash.
VERSION="know-me-api@$(cat /opt/km-api/VERSION)"
echo "Running ${VERSION}"

export DJANGO_SENTRY_RELEASE=${VERSION}

create_db_user() {
    # Note that the tabs in the following statement are used to preserve
    # indentation in the SQL statements.
    CREATE_ROLE=$(cat <<-EOF
		DO \$\$
		BEGIN
		    CREATE ROLE ${DJANGO_DB_USER} WITH LOGIN PASSWORD '${DJANGO_DB_PASSWORD}';
		    EXCEPTION WHEN OTHERS THEN
			    RAISE NOTICE 'not creating role ${DJANGO_DB_USER} -- it already exists';
			    ALTER ROLE ${DJANGO_DB_USER} WITH LOGIN PASSWORD '${DJANGO_DB_PASSWORD}';
		END
		\$\$;
	EOF
	)

    export PGPASSWORD=${DATABASE_ADMIN_PASSWORD}
	echo ${CREATE_ROLE} | psql --host ${DJANGO_DB_HOST} --port ${DJANGO_DB_PORT} --user ${DATABASE_ADMIN_USER} --dbname ${DJANGO_DB_NAME}
}

if [[ "$1" = 'background-jobs' ]]; then
    ${MANAGE_CMD} cleanemailconfirmations
    ${MANAGE_CMD} updatelegacyusers
    ${MANAGE_CMD} updatesubscriptions
    exit 0
fi

if [[ "$1" = 'migrate' ]]; then
    create_db_user
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
