from rest_framework import permissions
from .models import Client


class HasAPIKey(permissions.BasePermission):

    def has_permission(self, request, view):
        authorization = request.META.get("HTTP_AUTHORIZATION")
        if authorization is None:
            return False

        header = authorization.split()[0]
        if header != 'x-dispatch-api-key':
            return False

        key_value = authorization.split()[1]
        key = Client.objects.get(key=key_value)
        if not key:
            return False
        return True
