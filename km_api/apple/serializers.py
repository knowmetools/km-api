from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from rest_framework import serializers

from apple import receipts


class ReceiptTypeSerializer(serializers.Serializer):
    """
    Serializer used to determine the type of an Apple receipt.

    Apple receipts can be from the production environment, the test
    environment, or they can be invalid.
    """

    environment = serializers.CharField(
        help_text=_("The environment that the receipt belongs to."),
        read_only=True,
    )
    receipt_data = serializers.CharField(
        help_text=_(
            "The receipt data identifying the receipt to get the type of as a "
            "base64 encoded string."
        ),
        style={"base_template": "textarea.html"},
        write_only=True,
    )

    def validate(self, attrs):
        """
        Validate the provided receipt and determine which environment it
        belongs to.

        The complications here stem from the fact that if we receive a
        response indicating the receipt is valid, we have to determine
        if we queried against Apple's production or sandbox endpoint in
        order to return the correct environment.

        Args:
            attrs:
                The data to validate.

        Returns:
            The validated data.
        """
        receipt_data = attrs["receipt_data"]
        receipt_info = receipts.get_receipt_info(receipt_data)
        status = receipt_info["status"]

        if status == receipts.ReceiptCodes.PRODUCTION_RECEIPT:
            attrs["environment"] = "PRODUCTION"
        elif status == receipts.ReceiptCodes.TEST_RECEIPT:
            attrs["environment"] = "SANDBOX"
        elif status == receipts.ReceiptCodes.VALID:
            # Figure out if we validated against the production or
            # sandbox endpoint and set the environment accordingly.
            url = settings.APPLE_RECEIPT_VALIDATION_ENDPOINT
            prod_url = settings.APPLE_RECEIPT_VALIDATION_PRODUCTION_ENDPOINT

            if url == prod_url:
                attrs["environment"] = "PRODUCTION"
            else:
                attrs["environment"] = "SANDBOX"
        else:
            raise serializers.ValidationError(
                {"receipt_data": ugettext("The provided receipt is invalid.")}
            )

        return attrs
