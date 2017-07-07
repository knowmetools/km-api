from km_auth import serializers


def test_validate():
    """
    The serializer should be valid if a nonce is provided.
    """
    data = {
        'nonce': 's4mpl3n0nc3',
    }
    serializer = serializers.LayerIdentitySerializer(data=data)

    assert serializer.is_valid()
    assert serializer.data == {}
