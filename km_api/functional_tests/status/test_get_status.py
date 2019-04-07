def test_get_status(api_client):
    """
    The status endpoint should return a 200 response code since the test
    environment applies all migrations by default.
    """
    url = "/status/"
    response = api_client.get(url)

    assert response.status_code == 200
