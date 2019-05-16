import logging

from django.db import transaction
from django.utils import timezone
from django.utils.translation import ugettext, ugettext_lazy as _
from rest_email_auth.models import EmailAddress
from rest_framework import serializers

from know_me import models, subscriptions

logger = logging.getLogger(__name__)


RECEIPT_IN_USE = _("This receipt has already been used.")


class AppleReceiptInfoSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for getting information about an Apple receipt.
    """

    class Meta:
        fields = ("expiration_time",)
        model = models.AppleReceipt
        read_only_fields = ("__all__",)


class AppleReceiptQuerySerializer(serializers.Serializer):
    """
    Read-only serializer for responding to Apple receipt queries.
    """

    email = serializers.EmailField(
        help_text=_(
            "The primary email address of the Know Me user who is using the "
            "Apple receipt matching the provided receipt data."
        ),
        read_only=True,
    )
    is_used = serializers.BooleanField(
        help_text=_(
            "A boolean indicating if the provided data corresponds to an "
            "Apple receipt that is in use."
        ),
        read_only=True,
    )
    receipt_data = serializers.CharField(
        help_text=_(
            "The receipt data identifying the receipt to check for the "
            "existence of."
        ),
        write_only=True,
    )

    def __init__(self, *args, **kwargs):
        """
        Initialize cached properties.
        """
        super().__init__(*args, **kwargs)

        self._receipt_info = None

    def save(self):
        """
        Override ``save`` to do nothing as the data is not persistable.
        """
        pass

    def validate(self, attrs):
        """
        Validate the serializer's data.

        Args:
            attrs:
                The data to validate.

        Returns:
            The validated data.
        """
        try:
            receipt = models.AppleReceipt.objects.get(
                transaction_id=self._receipt_info.original_transaction_id
            )
            email = receipt.subscription.user.primary_email.email

            attrs["email"] = email
            attrs["is_used"] = True
        except models.AppleReceipt.DoesNotExist:
            attrs["email"] = None
            attrs["is_used"] = False

        return attrs

    def validate_receipt_data(self, receipt_data):
        """
        Ensure the provided receipt data corresponds to a valid Apple
        receipt.

        Args:
            receipt_data:
                The receipt data to validate.

        Returns:
            The validated receipt data.
        """
        try:
            self._receipt_info = subscriptions.validate_apple_receipt(
                receipt_data
            )
        except subscriptions.ReceiptException as e:
            raise serializers.ValidationError(code=e.code, detail=e.msg)

        return receipt_data


class AppleReceiptSerializer(serializers.ModelSerializer):
    """
    Serializer for an Apple receipt.
    """

    class Meta:
        fields = (
            "id",
            "time_created",
            "time_updated",
            "expiration_time",
            "receipt_data",
        )
        model = models.AppleReceipt
        read_only_fields = (
            "expiration_time",
            "id",
            "time_created",
            "time_updated",
        )

    def save(self, subscription):
        """
        Save the :class:`AppleReceipt` instance associated with the
        serializer.

        Args:
            subscription:
                The subscription to associate the Apple receipt being
                saved with.
        """
        subscription.is_active = self.instance.expiration_time > timezone.now()
        subscription.save()
        self.instance.subscription = subscription
        self.instance.save()

    def validate(self, data):
        """
        Validate that the provided receipt data corresponds to a valid
        Apple receipt for a subscription that we recognize.

        Args:
            data:
                The data to validate.

        Returns:
            The validated data.
        """
        self.instance = self.instance or models.AppleReceipt()
        self.instance.receipt_data = data["receipt_data"]

        try:
            self.instance.update_info()
        except subscriptions.ReceiptException as e:
            raise serializers.ValidationError(
                code=e.code, detail={"receipt_data": e.msg}
            )

        if (
            models.AppleReceipt.objects.exclude(pk=self.instance.pk)
            .filter(transaction_id=self.instance.transaction_id)
            .exists()
        ):
            raise serializers.ValidationError({"receipt_data": RECEIPT_IN_USE})

        return data


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for getting an overview of a user's Know Me premium
    subscription.
    """

    apple_receipt = AppleReceiptInfoSerializer()

    class Meta:
        fields = ("apple_receipt", "is_active", "is_legacy_subscription")
        model = models.Subscription
        read_only_fields = ("__all__",)


class SubscriptionTransferSerializer(serializers.Serializer):
    """
    Serializer for transferring a Know Me premium subscription to a
    different user.
    """

    recipient_email = serializers.EmailField(
        help_text=_(
            "The email address of the Know Me user that the requesting user's "
            "premium subscription should be transferred to."
        )
    )

    def __init__(self, *args, **kwargs):
        """
        Initialize cached values to ``None``.
        """
        super().__init__(*args, **kwargs)

        self._recipient_email_inst = None

    def save(self):
        """
        Transfer a subscription to the user who owns the provided email
        address.
        """
        owner = self.context["request"].user
        recipient = self._recipient_email_inst.user

        logger.info(
            "Transferring subscription %r from user %r to user %r",
            owner.know_me_subscription,
            owner.pk,
            recipient.pk,
        )

        with transaction.atomic():
            models.Subscription.objects.filter(user=recipient).delete()
            models.Subscription.objects.filter(user=owner).update(
                user=recipient
            )

    def validate(self, data):
        """
        Validate the transfer request as a whole.

        Args:
            data:
                The data to validate.

        Returns:
            The validated data.

        Raises:
            serializers.ValidationError:
                If the recipient is unable to receive a subscription
                transfer.
        """
        if not models.Subscription.objects.filter(
            is_active=True, user=self.context["request"].user
        ).exists():
            raise serializers.ValidationError(
                ugettext(
                    "You must have an active premium subscription in order to "
                    "transfer it to another user."
                )
            )

        if models.Subscription.objects.filter(
            is_active=True, user=self._recipient_email_inst.user
        ).exists():
            raise serializers.ValidationError(
                ugettext(
                    "The intended recipient already has an active premium "
                    "subscription."
                )
            )

        if models.AppleReceipt.objects.filter(
            subscription__user=self._recipient_email_inst.user
        ).exists():
            raise serializers.ValidationError(
                ugettext(
                    "The intended recipient has an Apple subscription that "
                    "must be removed before they can accept a transfer."
                )
            )

        return data

    def validate_recipient_email(self, email):
        """
        Validate the recipient's email address.

        Args:
            email:
                The email address to validate.

        Returns:
            The validated email address.

        Raises:
            serializers.ValidationError:
                If the provided email address does not exist or is not
                verified.
        """
        email_query = EmailAddress.objects.filter(
            email=email, is_verified=True
        )

        if not email_query.exists():
            raise serializers.ValidationError(
                ugettext("No Know Me user owns the provided email address.")
            )

        self._recipient_email_inst = email_query.get()

        return email
