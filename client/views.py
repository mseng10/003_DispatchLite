from django.http import JsonResponse
from client.models import Client, Template
from client.serializers import ClientSerializer, TemplatesSerializer,returnListOfURLS
from client.permissions import HasAPIKey
from rest_framework.decorators import permission_classes
from rest_framework import status

@permission_classes([HasAPIKey])
def client(request):
    key = request.META.get("HTTP_AUTHORIZATION").split()[1]
    if request.method == 'GET':
        client = Client.objects.get(key=key)
        serializer = ClientSerializer(client)
        return JsonResponse(serializer.data, safe=False,status=status.HTTP_200_OK)

@permission_classes([HasAPIKey])
def templates(request):
    if request.method == 'GET':
        templates = Template.objects.all()
        print(templates[0].url)
        serializer = TemplatesSerializer(data=templates, many=True)
        print(serializer.is_valid())
        print(serializer.errors)
        print(serializer.data)

        data = returnListOfURLS(serializer.data)

        return JsonResponse(data, safe=False,status=status.HTTP_200_OK)