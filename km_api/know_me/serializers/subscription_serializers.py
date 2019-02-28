from rest_framework import serializers

from know_me import models, subscriptions


class AppleSubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for an Apple subscription.
    """

    class Meta:
        fields = (
            "id",
            "time_created",
            "time_updated",
            "expiration_time",
            "receipt_data",
        )
        model = models.SubscriptionAppleData

    def validate(self, data):
        """
        Ensure the provided receipt data corresponds to a valid Apple
        receipt.

        Returns:
            The validated data.
        """
        validated_data = data.copy()
        receipt_data = validated_data["receipt_data"]

        try:
            receipt = subscriptions.validate_apple_receipt(receipt_data)
        except subscriptions.ReceiptException as e:
            raise serializers.ValidationError(
                code=e.code, detail={"receipt_data": e.msg}
            )

        validated_data["expiration_time"] = receipt.expires_date

        return validated_data
