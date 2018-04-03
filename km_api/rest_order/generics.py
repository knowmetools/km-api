from rest_framework import generics

from rest_order import mixins


class SortView(mixins.SortModelMixin, generics.GenericAPIView):
    def put(self, request, *args, **kwargs):
        return self.sort(request, *args, **kwargs)
