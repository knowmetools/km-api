from push_notifications.api.rest_framework import APNSDeviceSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class APNSDeviceListView(generics.ListCreateAPIView):
    """
    get:
    List the specified user's registered APNS devices.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = APNSDeviceSerializer

    def get_queryset(self):
        """
        Get a list of the requesting user's APNS devices.
        """
        return self.request.user.apnsdevice_set.all()

    def perform_create(self, serializer):
        """
        Create a new APNS device for the requesting user.

        Args:
            serializer:
                An instance of the view's serializer class containing
                the data from the request.
        """
        serializer.save(user=self.request.user)
