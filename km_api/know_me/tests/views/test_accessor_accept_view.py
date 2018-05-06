from unittest import mock

from rest_framework import status

from know_me import models, views


@mock.patch(
    'know_me.views.DRYGlobalPermissions.has_object_permission',
    autospec=True,
)
def test_check_object_permissions(
        mock_dry_permissions,
        km_user_accessor_factory):
    """
    The view should check the permissions on the model.
    """
    accessor = km_user_accessor_factory()
    view = views.AccessorAcceptView()

    with mock.patch.object(
        accessor,
        'has_object_accept_permission',
        autospec=True,
        return_value=True,
    ) as mock_accept_perm:
        view.check_object_permissions(None, accessor)

    assert mock_dry_permissions.call_count == 1
    assert mock_accept_perm.call_count == 1


@mock.patch(
    'know_me.views.DRYGlobalPermissions.has_object_permission',
    autospec=True,
)
@mock.patch(
    'know_me.views.AccessorAcceptView.permission_denied',
    autospec=True,
)
def test_check_object_permissions_no_accept_perm(
        mock_permission_denied,
        mock_dry_permissions,
        km_user_accessor_factory):
    """
    If the requesting user doesn't have accept permissions on the
    accessor, an exception should be raised.
    """
    accessor = km_user_accessor_factory()
    view = views.AccessorAcceptView()

    with mock.patch.object(
        accessor,
        'has_object_accept_permission',
        autospec=True,
        return_value=False,
    ) as mock_accept_perm:
        view.check_object_permissions(None, accessor)

    assert mock_dry_permissions.call_count == 1
    assert mock_accept_perm.call_count == 1
    assert mock_permission_denied.call_count == 1


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
    view.request = view.initialize_request(request)

    response = view.post(request)

    accessor.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert accessor.is_accepted
