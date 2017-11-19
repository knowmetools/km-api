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
        # Since the docstring is used to generate the documentation, we
        # don't include one for this generic view.
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            self.post_save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
