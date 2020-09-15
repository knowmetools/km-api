from know_me.serializers import email_reminder_subscriber_serializers


def test_create(serializer_context, user_factory):
    """
    Saving a serializer containing valid data should create a new
    reminder_email_subscriber.
    """
    user = user_factory()
    data = {"is_subscribed": True, "schedule_frequency": "Daily"}

    serializer = email_reminder_subscriber_serializers.ReminderEmailSubscriberSerializer(  # noqa
        context=serializer_context, data=data
    )
    assert serializer.is_valid()

    serializer.save(user=user)
    reminder_email_subscriber = user.reminder_email_subscriber

    assert reminder_email_subscriber.is_subscribed == data["is_subscribed"]
    assert (
        reminder_email_subscriber.schedule_frequency
        == data["schedule_frequency"]
    )
    assert reminder_email_subscriber.subscription_uuid is not None


def test_serialize(
    serializer_context, user_factory, reminder_email_subscriber_factory
):
    """
    Test serializing email reminder subscriptions
    """
    subscriber = reminder_email_subscriber_factory()

    serializer = email_reminder_subscriber_serializers.ReminderEmailSubscriberSerializer(  # noqa
        subscriber, context=serializer_context
    )

    expected = {"is_subscribed": True, "schedule_frequency": "Weekly"}

    assert serializer.data["is_subscribed"] == expected["is_subscribed"]
    assert (
        serializer.data["schedule_frequency"] == expected["schedule_frequency"]
    )
    assert serializer.data["subscription_uuid"] is not None
