from django.http import JsonResponse
from client.models import Client, Template, Message, Batch
from client.serializers import ClientSerializer, TemplatesSerializer,returnListOfURLS,\
                               TemplateSerializer, CampaignSerializer, PopulationSerializer, CommunicationSerializer, MessageSerializer, BatchSerializer
from client.permissions import HasAPIKey
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
import os


if 'WEBSITE_HOSTNAME' in os.environ:
    url = 'finalurl'
else:
    url = 'http://127.0.0.1:8000/'



@permission_classes([HasAPIKey])
def client(request):
    key = request.META.get("HTTP_AUTHORIZATION").split()[1]
    if request.method == 'GET':
        client = Client.objects.get(key=key)
        serializer = ClientSerializer(client)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@permission_classes([HasAPIKey])
def templates(request):
    if request.method == 'GET':
        templates = Template.objects.all()
        serializer = TemplatesSerializer(data=templates, many=True)
        data = returnListOfURLS(serializer.data)
        return JsonResponse(data, safe=False, status=status.HTTP_200_OK)


@permission_classes([HasAPIKey])
def template(request, id):
    if request.method == 'GET':
        template = Template.objects.get(id=id)
        if template:
            serializer = TemplateSerializer(template)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        return JsonResponse('Template not found', safe=False, status=status.HTTP_404_NOT_FOUND)


@permission_classes([HasAPIKey])
@parser_classes([JSONParser])
@api_view(['POST'])
def campaign(request, format=None):
    serializer = CampaignSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
        return JsonResponse(obj.url, safe=False, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse("Bad Request", safe=False, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([HasAPIKey])
@parser_classes([JSONParser])
@api_view(['POST'])
def communication(request, campaign_id):
    campaign = url + 'campaigns/' + str(campaign_id)
    serializer = CommunicationSerializer(data=request.data)
    if serializer.is_valid():
        communication = serializer.save()
        communication.campaign = campaign
        communication.save()
        return JsonResponse(communication.url, safe=False, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([HasAPIKey])
@parser_classes([JSONParser])
@api_view(['POST'])
def adhoc_communication(request, communication_id):
    pass


@permission_classes([HasAPIKey])
@parser_classes([JSONParser])
@api_view(['POST'])
def population(request, format=None):
    serializer = PopulationSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
        return JsonResponse(obj.url, safe=False, status=status.HTTP_201_CREATED)
    else:
        for value in serializer.errors:
            for v in serializer.errors[value]:
                if 'population with this name already exists.' == v:
                    return JsonResponse("Conflict - Population name already in use for client", safe=False,
                                        status=status.HTTP_409_CONFLICT)
        return JsonResponse("Bad Request", safe=False, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([HasAPIKey])
def messages(request, member_id):
    if request.method == 'GET':
        try:
            message = Message.objects.get(memberId=member_id)
            serializer = MessageSerializer(message)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            return JsonResponse('Message not found', safe=False, status=status.HTTP_404_NOT_FOUND)


@permission_classes([HasAPIKey])
def batches(request, id):
    breakpoint()
    if request.method == 'GET':
        try:
            batch = Batch.objects.get(id=id)
            serializer = BatchSerializer(batch)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except Batch.DoesNotExist:
            return JsonResponse('Batch not found', safe=False, status=status.HTTP_404_NOT_FOUND)


