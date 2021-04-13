from rest_framework import serializers
from client.models import Client, Template, Campaign, Population, Message, Batch
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


class TemplateSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Template
        fields = ('client',
                  'comments',
                  'content',
                  'description',
                  'dynamic',
                  'id',
                  'name',
                  'tags',
                  'type')

    def get_comments(self, instance):
        return (instance.comments.url if instance.comments != '' else None)

    def get_content(self, instance):
        return (instance.content.url if instance.content != '' else None)

    def get_description(self, instance):
        return (instance.description.url if instance.description != '' else None)


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('name',
                  'tags',
                  'productionMode',
                  'communications')

        # Required for post requests from Dispatch API, also they cannot be null
        extra_kwargs = {'name': {'required': True, 'allow_null': False},
                        'productionMode': {'required': True, 'allow_null': False}}


class PopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Population
        fields = ('name',
                  'description',
                  'dataSourceType',
                  'parameterized',
                  'archived',
                  'hidden',
                  'tags',
                  'manualEmailList'
                  )

        # Required for post requests from Dispatch API, also they cannot be null
        extra_kwargs = {'name': {'required': True, 'allow_null': False},
                        'dataSourceType': {'required': True, 'allow_null': False}}


# rough MessageSerializer
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('memberId',
                  'type',
                  'excluded',
                  'member',
                  'sentDate',
                  'batch',
                  'receiptDate',
                  'fromName',
                  'fromAddress',
                  'fromPhone',
                  'toAddress',
                  'toName',
                  'toPhone',
                  'subject'
                  )


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'
