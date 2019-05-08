from rest_framework import generics, status

from apple import serializers


class ReceiptTypeQueryView(generics.CreateAPIView):
    """
    post:
    Get the type of an Apple receipt. If the provided receipt data
    corresponds to a receipt that is valid in either the production or
    test environments, then the `environment` key of the response will
    be given as `PRODUCTION` or `SANDBOX`, respectively.

    An invalid receipt will cause a 400 response.
    """

    serializer_class = serializers.ReceiptTypeSerializer

    def create(self, *args, **kwargs):
        """
        Override the parent class' ``create`` method to set the status
        code of the response to 200.
        """
        response = super().create(*args, **kwargs)
        response.status_code = status.HTTP_200_OK

        return response

    def perform_create(self, serializer):
        """
        Override the method to not save the serializer. There is no data
        to save, we just use the ``POST`` request so we can submit a
        large body.
        """
        pass
