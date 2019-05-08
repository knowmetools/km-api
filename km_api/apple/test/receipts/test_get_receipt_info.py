from apple.receipts import get_receipt_info, ReceiptCodes


def test_get_apple_receipt_info_retry(apple_receipt_client):
    """
    If the initial response indicates the request should be retried, the
    method should honor that.
    """
    data = "valid-receipt"
    expected_status = {"status": ReceiptCodes.VALID}
    apple_receipt_client.enqueue_status(data, {"is-retryable": True})
    apple_receipt_client.enqueue_status(data, expected_status)

    result = get_receipt_info(data)

    assert result == expected_status


def test_get_apple_receipt_info_valid(apple_receipt_client):
    """
    Given a valid receipt data string, this method should return the
    JSON data returned by the Apple store.
    """
    data = "valid-receipt"
    expected = {"status": ReceiptCodes.VALID}
    apple_receipt_client.enqueue_status(data, expected)

    result = get_receipt_info(data)

    assert result == expected
