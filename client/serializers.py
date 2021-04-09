from rest_framework import serializers
from client.models import Client, Template
import collections

def returnListOfURLS(data):
    orderedDictionary = collections.OrderedDict()
    list = []
    for key in data:
        for key, value in key.items():
            list.append(value)
    orderedDictionary = list
    return orderedDictionary

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id',
                  'name',
                  'campaigns',
                  'templates',
                  'populations',
                  'suppressionLists',
                  'archives')

class TemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('url',)