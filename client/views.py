from django.http import JsonResponse
from client.models import *
from client.serializers import *
from client.permissions import HasAPIKey
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
import os
import pdb


if 'WEBSITE_HOSTNAME' in os.environ:
    url = 'https://dispatchlite.azurewebsites.net/'
else:
    url = 'http://127.0.0.1:8000/'



@permission_classes([HasAPIKey])
@api_view(['GET'])
def client(request):
    key = request.META.get("HTTP_AUTHORIZATION").split()[1]
    if request.method == 'GET':
        client = Client.objects.get(key=key)
        serializer = ClientSerializer(client)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@permission_classes([HasAPIKey])
@api_view(['GET'])
def templates(request):
    templates = Template.objects.all()
    serializer = TemplatesSerializer(templates, many=True)
    data = returnListOfURLS(serializer.data)
    return JsonResponse(data, safe=False, status=status.HTTP_200_OK)


@permission_classes([HasAPIKey])
@api_view(['GET'])
def template(request, id):
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
    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        return JsonResponse("Bad Request", safe=False, status=status.HTTP_400_BAD_REQUEST)
    campaign = campaign.url
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
    serializer = MemberSerializer(data=request.data['members'], many=True)
    if not serializer.is_valid():
        return JsonResponse("There was some problem parsing your array of members.", safe=False, status=status.HTTP_400_BAD_REQUEST)
    try:
        communication = Communication.objects.get(id=communication_id)
    except Communication.DoesNotExist:
        return JsonResponse("Communication not found", safe=False, status=status.HTTP_404_NOT_FOUND)
    try:
        include_batch_response = request.data['includeBatchResponse']
    except KeyError:
        include_batch_response = False
    batch = Batch().create_from_adhoc(request.data['members'], communication.url)
    for member in batch.members:
        batch_data = BatchSerializer(batch).data
        Message().create_from_adhoc(member=member, batch=batch_data, communication=communication)
    if include_batch_response:
        return JsonResponse(batch.url, safe=False, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse("Successful response", safe=False, status=status.HTTP_200_OK)


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
@api_view(['GET'])
def messages(request, member_id):
    try:
        message = Message.objects.get(memberId=member_id)
        serializer = MessageSerializer(message)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Message.DoesNotExist:
        return JsonResponse('Message not found', safe=False, status=status.HTTP_404_NOT_FOUND)


@permission_classes([HasAPIKey])
@api_view(['GET'])
def batches(request, id):
    try:
        batch = Batch.objects.get(id=id)
        serializer = BatchSerializer(batch)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Batch.DoesNotExist:
        return JsonResponse('Batch not found', safe=False, status=status.HTTP_404_NOT_FOUND)
