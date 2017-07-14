from unittest import mock

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

    with mock.patch(
            'account.models.EmailConfirmation.send_confirmation',
            autospec=True) as mock_confirm:
        email = serializer.save()

    assert email.email == data['email']
    assert not email.verified
    assert email.confirmations.count() == 1
    assert mock_confirm.call_count == 1


def test_create_primary(api_rf, email_factory, user_factory):
    """
    A user should not be able to set an email address as primary when
    it's created.
    """
    user = user_factory()
    email_factory(primary=True, user=user, verified=True)

    api_rf.user = user
    request = api_rf.get('/')

    data = {
        'email': 'newprimary@example.com',
        'primary': True,
    }

    serializer = serializers.EmailSerializer(
        context={'request': request},
        data=data)

    assert not serializer.is_valid()


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


def test_update_primary(email_factory):
    """
    Setting a verified email address to the primary address should
    update all of the user's emails.
    """
    # We have to create a dummy email first, since the first email for a
    # user is always set to the primary.
    dummy = email_factory()
    email = email_factory(primary=False, user=dummy.user, verified=True)

    data = {
        'primary': True,
    }

    serializer = serializers.EmailSerializer(email, data=data, partial=True)
    assert serializer.is_valid()

    with mock.patch(
            'account.models.EmailAddress.set_primary',
            autospec=True) as mock_primary:
        serializer.save()

    assert mock_primary.call_count == 1


def test_update_primary_unverified(email_factory):
    """
    An unverified email address should not be able to be set as the
    primary address.
    """
    # We have to create a dummy email first, since the first email for a
    # user is always set to the primary.
    dummy = email_factory()
    email = email_factory(primary=False, user=dummy.user, verified=False)

    data = {
        'primary': True,
    }

    serializer = serializers.EmailSerializer(email, data=data, partial=True)

    assert not serializer.is_valid()
