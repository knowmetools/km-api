from unittest import mock

from rest_framework import status

from status import views


def test_health_check_no_migrations(db):
    """
    If there are no migrations that have not been applied, the status
    endpoint should return a 200 status.
    """
    with mock.patch(
        "status.views.MigrationExecutor.migration_plan",
        autospec=True,
        return_value=None,
    ):
        response = views.health_check(None)

    assert response.status_code == status.HTTP_200_OK


def test_health_check_with_migrations(db):
    """
    If there are un-applied migrations, the status endpoint should
    return a 503 response.
    """
    # We need some sort of mock plan. Don't really know what they look
    # like though.
    mock_plan = {"foo": "bar"}
    with mock.patch(
        "status.views.MigrationExecutor.migration_plan",
        autospec=True,
        return_value=mock_plan,
    ):
        response = views.health_check(None)

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
