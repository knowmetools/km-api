from rest_framework.response import Response


class SortModelMixin(object):
    sort_child_name = None
    sort_parent = None
    sort_serializer = None

    def get_sort_serializer(self, *args, **kwargs):
        serializer_class = self.sort_serializer
        kwargs["context"] = self.get_serializer_context()

        return serializer_class(*args, **kwargs)

    def sort(self, request, *args, **kwargs):
        parent_pk = kwargs.get("pk", None)
        parent = self.sort_parent.objects.get(pk=parent_pk)

        serializer = self.get_sort_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(parent)

        collection = getattr(parent, self.sort_child_name).all()
        serializer = self.get_serializer(collection, many=True)

        return Response(serializer.data)
