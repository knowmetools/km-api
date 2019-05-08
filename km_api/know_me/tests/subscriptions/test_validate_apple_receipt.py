from unittest import mock

from know_me import subscriptions


def test_validate_apple_receipt():
    """
    The function should act as a wrapper for ``get_apple_receipt_info``
    and ``validate_apple_receipt_info``.
    """
    receipt_data = "test-data"

    with mock.patch(
        "know_me.subscriptions.get_receipt_info", autospec=True
    ) as mock_get_info, mock.patch(
        "know_me.subscriptions.validate_apple_receipt_response", autospec=True
    ) as mock_validate:
        result = subscriptions.validate_apple_receipt(receipt_data)

    assert mock_get_info.call_count == 1
    assert mock_get_info.call_args[0] == (receipt_data,)
    assert mock_validate.call_count == 1
    assert mock_validate.call_args[0] == (mock_get_info.return_value,)
    assert result == mock_validate.return_value
