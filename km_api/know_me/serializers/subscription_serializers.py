from rest_framework import serializers

from know_me import models


class AppleSubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for an Apple subscription.
    """

    class Meta:
        fields = ('id', 'time_created', 'time_updated', 'receipt_data')
        model = models.SubscriptionAppleData
