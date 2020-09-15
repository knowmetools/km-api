from know_me import models


def test_create(user_factory):
    """
    Test creating a legacy user.
    """
    sub1 = models.ReminderEmailSubscriber.objects.create(user=user_factory())
    assert sub1.is_subscribed

    sub2 = models.ReminderEmailSubscriber.objects.create(user=user_factory())
    assert sub1.subscription_uuid != sub2.subscription_uuid
