""" Generic RESTful views.
"""

from rest_framework import generics, status
from rest_framework.response import Response


class SerializerSaveView(generics.GenericAPIView):
    """
    View for saving a serializer using POST data
    """

    def post_save(self):
        """
        Performed after the serializer is saved.
        """
        pass

    def post(self, request):
        """
        Save a serializer with the given data.

        Args:
            request:
                The request being made.

        Returns:
            A response with a status code indicating if the request was
            succesful.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            self.post_save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
