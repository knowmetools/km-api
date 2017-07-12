import pytest

from account import models, serializers


def test_save_valid_key(email_confirmation_factory):
    """
    If a serializer with a valid key is saved, the email that the
    confirmation points to should be verified, and the confirmation
    should be deleted.
    """
    confirmation = email_confirmation_factory()
    user = confirmation.user

    data = {
        'key': confirmation.key,
    }

    serializer = serializers.EmailConfirmationSerializer(data=data)
    assert serializer.is_valid()

    serializer.save()
    user.refresh_from_db()

    assert models.EmailConfirmation.objects.count() == 0
    assert user.email_verified


@pytest.mark.django_db
def test_validate_unknown_key():
    """
    If the key given to the serializer has no corresponding email
    confirmation, the serializer should not be valid.
    """
    data = {
        'key': 'randomkey',
    }

    serializer = serializers.EmailConfirmationSerializer(data=data)

    assert not serializer.is_valid()
