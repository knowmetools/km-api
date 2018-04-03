from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class BaseOrderingSerializer(serializers.Serializer):
    """
    Serializer to order a model with respect to a foreign key owner.
    """
    order = serializers.ListField(
        child=serializers.IntegerField(),
        help_text=_("A list of the IDs of the collection's items in the "
                    "desired order."))

    sort_child = None

    def save(self, sort_parent):
        related_name = self.sort_child.__name__.lower()
        set_order = getattr(sort_parent, 'set_{}_order'.format(related_name))

        set_order(self.validated_data['order'])


def create_sort_serializer(child_model):
    class BoundOrderingSerializer(BaseOrderingSerializer):
        sort_child = child_model

    return BoundOrderingSerializer
