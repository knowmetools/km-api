import hashlib
import logging

from django.utils.translation import ugettext
from rest_framework import serializers

from know_me import models, subscriptions


logger = logging.getLogger(__name__)


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

        data_hash = hashlib.sha256(receipt_data.encode()).hexdigest()
        if models.SubscriptionAppleData.objects.filter(
            receipt_data_hash=data_hash
        ).exists():
            logger.warning(
                "Duplicate Apple receipt submitted with hash: %s", data_hash
            )

            raise serializers.ValidationError(
                {
                    "receipt_data": ugettext(
                        "This receipt has already been used."
                    )
                }
            )

        try:
            receipt = subscriptions.validate_apple_receipt(receipt_data)
        except subscriptions.ReceiptException as e:
            raise serializers.ValidationError(
                code=e.code, detail={"receipt_data": e.msg}
            )

        validated_data["expiration_time"] = receipt.expires_date

        return validated_data
