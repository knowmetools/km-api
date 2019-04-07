from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from django.http import HttpResponse


def health_check(request):
    """
    get:
    Check the status of the application. The application can be
    unhealthy if it depends on database migrations that have not been
    applied yet.
    """
    # The following code is taken from:
    # https://engineering.instawork.com/elegant-database-migrations-on-ecs-74f3487da99f
    executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
    status = 503 if plan else 200

    return HttpResponse(status=status)
