from know_me import subscriptions


class ReceiptCode:
    VALID = 0


def test_get_apple_receipt_info_retry(apple_receipt_client):
    """
    If the initial response indicates the request should be retried, the
    method should honor that.
    """
    data = "valid-receipt"
    expected_status = {"status": ReceiptCode.VALID}
    apple_receipt_client.enqueue_status(data, {"is-retryable": True})
    apple_receipt_client.enqueue_status(data, expected_status)

    result = subscriptions.get_apple_receipt_info(data)

    assert result == expected_status


def test_get_apple_receipt_info_valid(apple_receipt_client):
    """
    Given a valid receipt data string, this method should return the
    JSON data returned by the Apple store.
    """
    data = "valid-receipt"
    expected = {"status": ReceiptCode.VALID}
    apple_receipt_client.enqueue_status(data, expected)

    result = subscriptions.get_apple_receipt_info(data)

    assert result == expected
