from unittest import mock

from rest_framework import status

from know_me import models, views


@mock.patch(
    'know_me.views.DRYPermissions.has_object_permission',
    autospec=True)
def test_check_object_permissions(mock_dry_permissions, api_rf):
    """
    The view should check the permissions on the model.
    """
    view = views.AccessorAcceptView()

    view.check_object_permissions(None, None)

    assert mock_dry_permissions.call_count == 1


def test_get_queryset(km_user_accessor_factory):
    """
    The view should operate on all accessors.
    """
    km_user_accessor_factory()
    km_user_accessor_factory()
    km_user_accessor_factory()

    view = views.AccessorAcceptView()
    expected = models.KMUserAccessor.objects.all()

    assert list(view.get_queryset()) == list(expected)


def test_post(api_rf, km_user_accessor_factory, user_factory):
    """
    Sending a POST request to the view should mark the accessor as
    accepted.
    """
    user = user_factory()
    accessor = km_user_accessor_factory(
        is_accepted=False,
        user_with_access=user)

    api_rf.user = user
    request = api_rf.post('/', {})

    view = views.AccessorAcceptView()
    view.kwargs = {
        'pk': accessor.pk,
    }
    view.request = request

    response = view.post(request)

    accessor.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert accessor.is_accepted
