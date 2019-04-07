from know_me import views
from know_me.serializers import subscription_serializers


def test_get_serializer_class():
    """
    Test which serializer class is used by the view.
    """
    view = views.SubscriptionTransferView()
    expected = subscription_serializers.SubscriptionTransferSerializer

    assert view.get_serializer_class() == expected
