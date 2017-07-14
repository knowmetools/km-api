from account import serializers


def test_create_email(api_rf, user_factory):
    """
    Test creating a new email address.
    """
    user = user_factory()

    api_rf.user = user
    request = api_rf.get('/')

    data = {
        'email': 'mycoolemail@example.com',
    }

    serializer = serializers.EmailSerializer(
        context={'request': request},
        data=data)
    assert serializer.is_valid()

    email = serializer.save()

    assert email.email == data['email']
    assert not email.verified


def test_serialize_email(email_factory):
    """
    Test serializing an email address.
    """
    email = email_factory()
    serializer = serializers.EmailSerializer(email)

    expected = {
        'id': email.id,
        'email': email.email,
        'verified': email.verified,
        'primary': email.primary,
    }

    assert serializer.data == expected


def test_update_email(email_factory):
    """
    An email's address should not be able to be updated.
    """
    email = email_factory(email='old@example.com')
    data = {
        'email': 'new@example.com',
    }

    serializer = serializers.EmailSerializer(email, data=data, partial=True)

    assert not serializer.is_valid()
