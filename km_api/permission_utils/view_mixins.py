# Taken from:
# https://github.com/dbkaplan/dry-rest-permissions/issues/39#issuecomment-287345071


class ActionMixin:
    """
    This mixin adds an ``.action`` attribute to the view based on the
    ``action_map`` attribute, similar to the way a ``ViewSet`` does it.

    Example::

        class UserDetail(ActionMixin, generics.RetrieveUpdateAPIView):
            queryset = models.User.objects.all()
            serializer_class = serializers.UserSerializer
            action_map = {
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
            }

    """
    def initialize_request(self, request, *args, **kwargs):
        """
        Set the `.action` attribute on the view,
        depending on the request method.
        """
        request = super().initialize_request(request, *args, **kwargs)
        method = request.method.lower()
        if method == 'options':
            # This is a special case as we always provide handling for
            # the options method in the base `View` class. Unlike the
            # other explicitly defined actions, 'metadata' is implicit.
            self.action = 'metadata'
        else:
            self.action = self.action_map.get(method)
        return request


class DocumentActionMixin(ActionMixin):
    """
    Add an ``.action`` attribute to a document type view.
    """
    action_map = {
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }


class CollectionActionMixin(ActionMixin):
    """
    Add an ``.action`` attribute to a collection type view.
    """
    action_map = {
        'get': 'list',
        'post': 'create',
    }
