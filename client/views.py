from django.http import JsonResponse
from client.models import Client, Template, Campaign
from client.serializers import ClientSerializer, TemplatesSerializer,returnListOfURLS,\
                               TemplateSerializer, CampaignSerializer
from client.permissions import HasAPIKey
from rest_framework.decorators import permission_classes,api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes

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

@permission_classes([HasAPIKey])
def template(request,id):
    if request.method == 'GET':
        template = Template.objects.get(id=id)
        if template:
            serializer = TemplateSerializer(template)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        return JsonResponse('Template not found',safe=False, status=status.HTTP_404_NOT_FOUND)

@permission_classes([HasAPIKey])
@csrf_exempt
@parser_classes([JSONParser])
@api_view(['POST'])
def campaign(request, format=None):
    print(request)
    serializer = CampaignSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
        return JsonResponse(obj.url, safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse("Bad Request", safe=False, status=status.HTTP_400_BAD_REQUEST)
