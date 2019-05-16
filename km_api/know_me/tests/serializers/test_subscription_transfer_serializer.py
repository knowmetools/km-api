import pytest
from rest_framework.exceptions import ValidationError

from know_me import models
from know_me.serializers import subscription_serializers


def test_save(api_rf, subscription_factory, user_factory):
    """
    Given a user with an active subscription and the email address of a
    user without an active subscription, saving the serializer should
    transfer the subscription between the two users.
    """
    subscription = subscription_factory(is_active=True)
    user = subscription.user
    request = api_rf.get("/")
    request.user = user
    recipient = user_factory()

    serializer = subscription_serializers.SubscriptionTransferSerializer(
        context={"request": request},
        data={"recipient_email": recipient.primary_email.email},
    )
    assert serializer.is_valid()

    serializer.save()
    user.refresh_from_db()
    recipient.refresh_from_db()

    assert not hasattr(user, "know_me_subscription")
    assert recipient.know_me_subscription == subscription


def test_save_recipient_inactive_subscription(
    api_rf, subscription_factory, user_factory
):
    """
    If the recipient has an inactive subscription, it should be deleted
    during the transfer process.
    """
    subscription = subscription_factory(is_active=True)
    user = subscription.user
    api_rf.user = user
    request = api_rf.get("/")

    recipient = user_factory()
    recipient_subscription = subscription_factory(
        is_active=False, user=recipient
    )

    serializer = subscription_serializers.SubscriptionTransferSerializer(
        context={"request": request},
        data={"recipient_email": recipient.primary_email.email},
    )
    assert serializer.is_valid()

    serializer.save()

    assert not models.Subscription.objects.filter(
        pk=recipient_subscription.pk
    ).exists()


def test_validate_recipient_email_nonexistent(db):
    """
    If the provided recipient email does not exist in our database, a
    validation error should be raised.
    """
    serializer = subscription_serializers.SubscriptionTransferSerializer()

    with pytest.raises(ValidationError):
        serializer.validate_recipient_email("does-not-exist@example.com")


def test_validate_recipient_email_unverified(email_factory):
    """
    If the provided recipient email has not been verified, a validation
    error should be raised.
    """
    email = email_factory(is_verified=False)
    serializer = subscription_serializers.SubscriptionTransferSerializer()

    with pytest.raises(ValidationError):
        serializer.validate_recipient_email(email.email)


def test_validate_active_premium_subscription(api_rf, user_factory):
    """
    If the recipient has an active premium subscription, a validation
    error should be raised.
    """
    owner = user_factory(has_premium=True)
    api_rf.user = owner
    user = user_factory(has_premium=True)

    serializer = subscription_serializers.SubscriptionTransferSerializer(
        context={"request": api_rf.post("/")}
    )
    serializer.validate_recipient_email(user.primary_email.email)

    with pytest.raises(ValidationError):
        serializer.validate({"recipient_email": user.primary_email.email})


def test_validate_apple_data(api_rf, apple_receipt_factory, user_factory):
    """
    If the recipient has an Apple receipt for a premium subscription on
    file, then validation should fail.
    """
    owner = user_factory(has_premium=True)
    api_rf.user = owner
    receipt = apple_receipt_factory(subscription__is_active=False)
    user = receipt.subscription.user

    serializer = subscription_serializers.SubscriptionTransferSerializer(
        context={"request": api_rf.post("/")}
    )
    serializer.validate_recipient_email(user.primary_email.email)

    with pytest.raises(ValidationError):
        serializer.validate({"recipient_email": user.primary_email.email})


def test_validate_inactive_premium_subscription(
    api_rf, subscription_factory, user_factory
):
    """
    If the recipient has an associated subscription but it is inactive,
    validation should pass.
    """
    owner = user_factory(has_premium=True)
    api_rf.user = owner
    subscription = subscription_factory(is_active=False)

    serializer = subscription_serializers.SubscriptionTransferSerializer(
        context={"request": api_rf.post("/")}
    )
    serializer.validate_recipient_email(subscription.user.primary_email.email)

    result = serializer.validate(
        {"recipient_email": subscription.user.primary_email.email}
    )
    expected = {"recipient_email": subscription.user.primary_email.email}

    assert result == expected


def test_validate_owner_inactive_subscription(
    api_rf, subscription_factory, user_factory
):
    """
    If the user initiating the transfer has an inactive subscription,
    validation should fail.
    """
    owner = user_factory()
    subscription_factory(is_active=False, user=owner)
    api_rf.user = owner
    recipient = user_factory()

    serializer = subscription_serializers.SubscriptionTransferSerializer(
        context={"request": api_rf.post("/")}
    )
    serializer.validate_recipient_email(recipient.primary_email.email)

    with pytest.raises(ValidationError):
        serializer.validate({"recipient_email": recipient.primary_email.email})


def test_validate_owner_no_subscription(api_rf, user_factory):
    """
    If the user initiating the transfer does not have a subscription,
    validation should fail.
    """
    owner = user_factory()
    api_rf.user = owner
    recipient = user_factory()

    serializer = subscription_serializers.SubscriptionTransferSerializer(
        context={"request": api_rf.post("/")}
    )
    serializer.validate_recipient_email(recipient.primary_email.email)

    with pytest.raises(ValidationError):
        serializer.validate({"recipient_email": recipient.primary_email.email})
