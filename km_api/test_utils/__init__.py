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
