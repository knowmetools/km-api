import hashlib


def uses_permission_class(view, permission_class):
    """
    Determine if the provided view uses a given permission class.

    Args:
        view:
            The view instance to test.
        permission_class:
            The permission class to test for the presence of.

    Returns:
        A boolean indicating if the provided view uses the given
        permission class.
    """
    return any(
        isinstance(perm, permission_class) for perm in view.get_permissions()
    )


def receipt_data_hash(data):
    """
    Get the hash of some receipt data.

    Args:
        data:
            The receipt data to get the hash of.

    Returns:
        The SHA256 hash of the given data.
    """
    return hashlib.sha256(data.encode()).hexdigest()


def serialized_time(time):
    """
    Return a serialized version of a datetime instance in the format of
    a ``DateTimeField`` from Django Rest Framework.

    Logic taken from:
    https://github.com/encode/django-rest-framework/blob/6ea7d05979695cfb9db6ec3946d031b02a82952c/rest_framework/fields.py#L1217-L1221

    Args:
        time:
            The :class:`datetime.datetime` instance to serialize.

    Returns:
        A string containing the serialized version of the provided time.
    """
    formatted = time.isoformat()
    if formatted.endswith("+00:00"):
        formatted = formatted[:-6] + "Z"

    return formatted
