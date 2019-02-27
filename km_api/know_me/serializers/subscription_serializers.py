from rest_framework import serializers

from know_me import models, subscriptions


class AppleSubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for an Apple subscription.
    """

    class Meta:
        fields = ("id", "time_created", "time_updated", "receipt_data")
        model = models.SubscriptionAppleData

    def validate_receipt_data(self, receipt_data):
        """
        Ensure the provided receipt data corresponds to a valid Apple
        receipt.

        Returns:
            The validated receipt data.
        """
        try:
            subscriptions.validate_apple_receipt(receipt_data)
        except subscriptions.ReceiptException as e:
            raise serializers.ValidationError(code=e.code, detail=e.msg)

        return receipt_data
