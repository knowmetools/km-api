from rest_framework import status

from know_me import serializers, views


accessor_list_view = views.AccessorListView.as_view()


def test_get_sharing_list(api_rf, km_user_accessor_factory, km_user_factory):
    """
    Sending a GET request to the view should return a list of all the
    accessors for the given Know Me user.
    """
    km_user = km_user_factory()

    km_user_accessor_factory(km_user=km_user)
    km_user_accessor_factory()

    api_rf.user = km_user.user

    request = api_rf.get('/')
    response = accessor_list_view(request)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.KMUserAccessorSerializer(
        km_user.km_user_accessors.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data


def test_post_new_share(api_rf, km_user_factory):
    """
    Sending a POST request should create a new accessor with the
    provided permissions.
    """
    km_user = km_user_factory()
    api_rf.user = km_user.user

    data = {
        'can_write': True,
        'email': 'share@example.com',
        'has_private_profile_access': True,
    }

    request = api_rf.post('/', data)
    response = accessor_list_view(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert km_user.km_user_accessors.count() == 1

    accessor = km_user.km_user_accessors.get()

    assert accessor.can_write == data['can_write']
    assert accessor.email == data['email']
    assert accessor.has_private_profile_access == \
        data['has_private_profile_access']

    serializer = serializers.KMUserAccessorSerializer(
        accessor,
        context={'request': request})

    assert response.data == serializer.data
