from rest_framework import status

from test_utils import serialized_time


def test_list_entries_as_owner(
    api_client, enable_premium_requirement, journal_entry_factory, user_factory
):
    """
    Premium users should be able to list their own journal entries.
    """
    # Assume John is an existing premium user.
    password = "password"
    user = user_factory(
        first_name="John",
        has_premium=True,
        password="password",
        registration_signal__send=True,
    )
    api_client.log_in(user.primary_email.email, password)

    # If he has journal entries...
    entry = journal_entry_factory(km_user=user.km_user)

    # ...then he should be able to list them.
    url = f"/know-me/users/{user.km_user.pk}/journal-entries/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "count": 1,
        "previous": None,
        "next": None,
        "results": [
            {
                "id": entry.pk,
                "url": api_client.build_full_url(entry.get_absolute_url()),
                "created_at": serialized_time(entry.created_at),
                "updated_at": serialized_time(entry.updated_at),
                "attachment": None,
                "comment_count": 0,
                "comments_url": api_client.build_full_url(
                    entry.get_comments_url()
                ),
                "km_user_id": user.km_user.pk,
                "permissions": {"read": True, "write": True},
                "text": entry.text,
            }
        ],
    }
