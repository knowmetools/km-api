from rest_framework import status
from django.test import TestCase
from django.test import Client

import test_utils
from dry_rest_permissions.generics import DRYPermissions

from know_me import views
from know_me.serializers import email_reminder_subscriber_serializers


def test_web_invalid_link(reminder_email_subscriber_factory):
    """
    Sending a DELETE request to the endpoint should delete the reminder
    subscriber with the given UUID.
    """
    subscriber = reminder_email_subscriber_factory()

    email = subscriber.user.primary_email.email
    uuid = subscriber.subscription_uuid

    client = Client()
    test_case = TestCase()

    response = client.get(
        "/know-me/reminder-email-unsubscribe/wrong@fake.com/" + str(uuid) + "/"
    )
    test_case.assertEqual(response.status_code, 200)
    test_case.assertContains(response, "Invalid Link")

    fake_uuid = "a023ee69-a2bd-48d1-b85a-d4211ed7fbe9"
    if str(uuid) == fake_uuid:
        fake_uuid = "0023ee69-a2bd-48d1-b85a-d4211ed7fbe9"
    response = client.get(
        "/know-me/reminder-email-unsubscribe/" + email + "/" + fake_uuid + "/"
    )
    test_case.assertEqual(response.status_code, 200)
    test_case.assertContains(response, "Invalid Link")


def test_web_delete_reminder_subscriber(reminder_email_subscriber_factory):
    """
    Test unsubscribing to the reminder emails through the web link provided
    in the reminder emails
    """
    subscriber = reminder_email_subscriber_factory()

    email = subscriber.user.primary_email.email
    uuid = subscriber.subscription_uuid

    client = Client()
    test_case = TestCase()

    response = client.get(
        "/know-me/reminder-email-unsubscribe/" + email + "/" + str(uuid) + "/"
    )

    test_case.assertEqual(response.status_code, 200)
    test_case.assertContains(response, "Unsubscribed")


def test_get_permissions():
    """
    Test the permissions used by the view.
    """
    view = views.ReminderEmailSubscriberDetailView()

    assert test_utils.uses_permission_class(view, DRYPermissions)


def test_get_serializer_class():
    """
    Test which serializer class is used by the view.
    """
    view = views.ReminderEmailSubscriberListView()
    expected = (
        email_reminder_subscriber_serializers.ReminderEmailSubscriberSerializer
    )

    assert view.get_serializer_class() == expected


def test_get_reminder_email_subscriber(
    api_rf, reminder_email_subscriber_factory
):
    """
    Sending a GET request to the view should return the details of the
    accessor with the given ID.
    """
    reminder_subscriber = reminder_email_subscriber_factory()
    api_rf.user = reminder_subscriber.user

    request = api_rf.get("/")

    reminder_detail_view = views.ReminderEmailSubscriberDetailView.as_view()
    response = reminder_detail_view(request, pk=reminder_subscriber.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = email_reminder_subscriber_serializers.ReminderEmailSubscriberSerializer(  # noqa
        reminder_subscriber, context={"request": request}
    )

    assert response.data == serializer.data


def test_list_reminder_email_subscriber(
    api_rf, reminder_email_subscriber_factory
):
    """
    Sending a GET request to the view should return the details of the
    accessor with the given ID.
    """
    reminder_email_subscriber_factory()
    reminder_subscriber = reminder_email_subscriber_factory()
    api_rf.user = reminder_subscriber.user

    request = api_rf.get("/")

    reminder_list_view = views.ReminderEmailSubscriberListView.as_view()
    response = reminder_list_view(request, pk=reminder_subscriber.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = email_reminder_subscriber_serializers.ReminderEmailSubscriberSerializer(  # noqa
        reminder_subscriber, context={"request": request}
    )

    assert len(response.data) == 1
    assert response.data[0] == serializer.data


def test_create_reminder_email_subscriber(api_rf, user_factory):
    user = user_factory()
    api_rf.user = user

    request = api_rf.post("/")

    reminder_list_view = views.ReminderEmailSubscriberListView.as_view()
    response = reminder_list_view(request)

    assert response.status_code == 201
    assert response.data["is_subscribed"]
