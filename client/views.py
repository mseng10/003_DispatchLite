from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from client.models import Client
from client.serializers import ClientSerializer

# Create your views here.
@csrf_exempt
def client(request):
    if request.method == 'GET':
        snippets = Client.objects.get(key='41AZXWJ4aIfKPOlTFsVs')
        serializer = ClientSerializer(snippets)
        return JsonResponse(serializer.data, safe=False)