from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, status
from rest_framework.compat import set_rollback
from rest_framework.response import Response
from rest_framework.settings import api_settings


def convert_to_list(detail, key):
    result = list()
    if isinstance(detail, dict):
        for key, value in detail.items():
            result += convert_to_list(value, key)
    elif isinstance(detail, list) or isinstance(detail, tuple):
        for value in detail:
            result += convert_to_list(value, key)
    else:
        result.append({'message': detail, 'field': key})
    return result


def simple_exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.

    Return 400 errors like this:
    [
        {"field":"non_field_errors",
         "message":"User with this email already exist."},
        {"field":"field1",
         "message":"Someone other error."},
    ]

    """
    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        data = convert_to_list(exc.detail, api_settings.NON_FIELD_ERRORS_KEY)

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    elif isinstance(exc, Http404):
        msg = _('Not found.')
        data = {'detail': six.text_type(msg)}

        set_rollback()
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        msg = _('Permission denied.')
        data = {'detail': six.text_type(msg)}

        set_rollback()
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    return None
