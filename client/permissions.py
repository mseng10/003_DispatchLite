from rest_framework.permissions import BasePermission
from .models import Client


class HasAPIKey(BasePermission):

    def has_permission(self, request, view):
        authorization = request.META.get("HTTP_AUTHORIZATION")
        print(authorization)
        if authorization is None or len(authorization.split()) != 2:
            return False

        header = authorization.split()[0]
        if header != 'x-dispatch-api-key':
            return False

        key_value = authorization.split()[1]
        print(key_value)
        key = Client.objects.get(key=key_value)
        if not key:
            return False
        return True
