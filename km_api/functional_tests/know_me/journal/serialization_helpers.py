from functional_tests.serialization_helpers import (
    user_info,
    build_full_file_url,
)
from test_utils import serialized_time


def serialize_comment(comment, build_full_url, is_list=False):
    """
    Serialize a comment on a journal entry.
    """

    def serialize(value):
        return {
            "id": value.pk,
            "url": build_full_url(f"/know-me/journal/comments/{value.pk}/"),
            "created_at": serialized_time(value.created_at),
            "updated_at": serialized_time(value.updated_at),
            "permissions": {"destroy": True, "read": True, "write": False},
            "text": value.text,
            "user": user_info(value.user),
        }

    if is_list:
        return list(map(serialize, comment))

    return serialize(comment)


def serialize_entry(entry, build_full_url):
    """
    Serialize a journal entry.

    Args:
        entry:
            The entry to serialize.
        build_full_url:
            The method to use to convert an absolute URL into a full
            URI.

    Returns:
        The serialized version of the provided entry or entries.
    """
    return {
        "id": entry.pk,
        "url": build_full_url(f"/know-me/journal/entries/{entry.pk}/"),
        "created_at": serialized_time(entry.created_at),
        "updated_at": serialized_time(entry.updated_at),
        "attachment": build_full_file_url(entry.attachment, build_full_url),
        "comment_count": entry.comments.count(),
        "comments": serialize_comment(
            entry.comments.all(), build_full_url, is_list=True
        ),
        "comments_url": build_full_url(
            f"/know-me/journal/entries/{entry.pk}/comments/"
        ),
        "km_user_id": entry.km_user.pk,
        "permissions": {"read": True, "write": True},
        "text": entry.text,
    }
