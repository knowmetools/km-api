from account import models, serializers


def test_serialize_actions():
    """
    Test serializing the available verified action choices.
    """
    mock_action = models.EmailAction(1, 'label')
    serializer = serializers.EmailVerifiedActionSerializer(mock_action)

    expected = {
        'id': mock_action.id,
        'label': mock_action.label,
    }

    assert serializer.data == expected