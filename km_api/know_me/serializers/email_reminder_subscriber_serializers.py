from rest_framework import serializers

from know_me import models


class ReminderEmailSubscriberSerializer(serializers.ModelSerializer):
    """
    Serializer for ``ReminderEmailSubscriber`` instances.
    """

    class Meta:
        fields = ("is_subscribed", "schedule_frequency", "subscription_uuid")
        model = models.ReminderEmailSubscriber
        read_only_fields = ("subscription_uuid",)
