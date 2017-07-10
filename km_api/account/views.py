"""Views for the ``account`` module.
"""

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account import serializers


class PasswordChangeView(generics.GenericAPIView):
    """
    View for changing the user's password.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PasswordChangeSerializer

    def post(self, request):
        """
        Change the requesting user's password.

        Args:
            request:
                The request being made.

        Returns:
            A response with a status code indicating if the request was
            successful.
        """
        serializer = self.get_serializer(data=request.POST)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
