from know_me import serializers
from know_me.profile.factories import ProfileFactory
from know_me.profile.serializers import ProfileListSerializer


def test_serialize(
        api_rf,
        image,
        km_user_factory,
        serializer_context):
    """
    Test serializing a km_user.
    """
    km_user = km_user_factory(image=image)
    ProfileFactory(km_user=km_user)
    ProfileFactory(km_user=km_user)

    api_rf.user = km_user.user
    request = api_rf.get('/')


    serializer = serializers.KMUserDetailSerializer(
        km_user,
        context={'request': request})
    profile_serializer = ProfileListSerializer(
        km_user.profiles,
        context={'request': request},
        many=True)

    url = api_rf.get(km_user.get_absolute_url()).build_absolute_uri()
    category_url = km_user.get_media_resource_category_list_url(request)
    image_url = api_rf.get(km_user.image.url).build_absolute_uri()
    media_resource_request = api_rf.get(km_user.get_media_resource_list_url())
    profile_list_url = km_user.get_profile_list_url(request)

    expected = {
        'id': km_user.id,
        'url': url,
        'name': km_user.name,
        'quote': km_user.quote,
        'image': image_url,
        'media_resource_categories_url': category_url,
        'media_resources_url': media_resource_request.build_absolute_uri(),
        'profiles_url': profile_list_url,
        'profiles': profile_serializer.data,
        'permissions': {
            'read': km_user.has_object_read_permission(request),
            'write': km_user.has_object_write_permission(request),
        }
    }

    assert serializer.data == expected


def test_update(km_user_factory):
    """
    Saving a bound serializer with valid data should update the km_user
    the serializer is bound to.
    """
    km_user = km_user_factory(quote='Old quote.')
    data = {
        'quote': 'New quote.',
    }

    serializer = serializers.KMUserDetailSerializer(
        km_user,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    km_user.refresh_from_db()

    assert km_user.quote == data['quote']
