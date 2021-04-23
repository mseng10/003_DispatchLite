from rest_framework import serializers
from client.models import *
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
        return (instance.comments if instance.comments != '' else None)

    def get_content(self, instance):
        return (instance.content if instance.content != '' else None)

    def get_description(self, instance):
        return (instance.description if instance.description != '' else None)


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('id',
                  'name',
                  'tags',
                  'productionMode',
                  'communications')

        # Required for post requests from Dispatch API, also they cannot be null
        extra_kwargs = {'name': {'required': True, 'allow_null': False},
                        'productionMode': {'required': True, 'allow_null': False}}


class CommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communication
        fields = '__all__'

        # Required for post requests from Dispatch API, also they cannot be null
        extra_kwargs = {'email': {'required': True},
                        'destination': {'required': True},
                        'name': {'required': True}}

    def validate_email(self, value):
        try:
            value['fromAddress']
            value['fromName']
            value['subject']
        except KeyError:
            raise serializers.ValidationError("'email' must have fromAddress, fromName, and subject.")
        return value

    def validate_destinations(self, value):
        try:
            value[0]['bounceAddress']
            value[0]['linkTrackingDisabled']
            value[0]['openTrackingDisabled']
            value[0]['replyToAddress']
            value[0]['suppressionList']
            value[0]['type']
        except KeyError:
            raise serializers.ValidationError("Field 'destinations' must provide boundAddress, linkTrackingDisabled, openTrackingDisabled, replyToAddress, suppressionList, and type.")
        if len(value) != 1 or value[0]['type'] != 'SMTP':
            raise serializers.ValidationError("DispatchLite only support SMTP type destinations.")
        return value

    def validate(self, data):
        if data['type'] == 'EMAIL':
            try:
                data['email']
            except KeyError:
                raise serializers.ValidationError("'email' field must have data if 'type' is 'EMAIL'")
        else:
            raise serializers.ValidationError("DispatchLite only supports 'type' of 'EMAIL'")

        return data


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


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


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
