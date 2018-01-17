from rest_framework.exceptions import MethodNotAllowed


class MethodSerializerView(object):
    '''
    Utility class for get different serializer class by method.
    For example:
    method_serializer_classes = {
        ('GET'): MyModelListViewSerializer,
        ('PUT', 'PATCH'): MyModelCreateUpdateSerializer
    }
    '''
    method_serializer_classes = None

    def get_serializer_class(self):
        assert self.method_serializer_classes is not None, (
            'Expected view {} should contain method_serializer_classes '
            'to get right serializer class.'.format(self.__class__.__name__, )
        )

        # For swagger v0.3.x
        if self.request.method == 'OPTIONS':
            return None
        for methods, serializer_cls in self.method_serializer_classes.items():
            if isinstance(methods, list):
                if self.request.method in methods:
                    return serializer_cls
            else:
                if self.request.method == methods:
                    return serializer_cls

        raise MethodNotAllowed(self.request.method)