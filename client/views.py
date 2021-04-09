from django.http import JsonResponse
from client.models import Client
from client.serializers import ClientSerializer
from client.permissions import HasAPIKey
from rest_framework.decorators import permission_classes
from rest_framework import status

@permission_classes([HasAPIKey])
def client(request):
    key = request.META.get("HTTP_AUTHORIZATION").split()[1]
    if request.method == 'GET':
        snippets = Client.objects.get(key=key)
        serializer = ClientSerializer(snippets)
        return JsonResponse(serializer.data, safe=False,status=status.HTTP_200_OK)