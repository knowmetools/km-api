from rest_framework.reverse import reverse

from know_me import serializers


def test_serialize(profile_factory, serializer_context):
    """
    Test serializing a profile.
    """
    profile = profile_factory()
    serializer = serializers.ProfileDetailSerializer(
        profile,
        context=serializer_context)

    expected = {
        'id': profile.id,
        'url': reverse(
            'know-me:profile-detail',
            kwargs={'profile_pk': profile.pk},
            request=serializer_context['request']),
        'name': profile.name,
        'quote': profile.quote,
        'welcome_message': profile.welcome_message,
    }

    assert serializer.data == expected


def test_update(profile_factory):
    """
    Saving a bound serializer with valid data should update the profile
    the serializer is bound to.
    """
    profile = profile_factory(name='Jim')
    data = {
        'name': 'John',
    }

    serializer = serializers.ProfileDetailSerializer(
        profile,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    profile.refresh_from_db()

    assert profile.name == data['name']
