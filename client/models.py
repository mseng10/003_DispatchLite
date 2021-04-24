from django.db import models
import random
from django.utils.crypto import get_random_string
import os
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
import datetime

# from client.serializers import BatchSerializer

if 'WEBSITE_HOSTNAME' in os.environ:
    url = 'https://dispatchlite.azurewebsites.net/'
else:
    url = 'http://127.0.0.1:8001/'


# Create your models here.
class Client(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    campaigns = models.CharField(max_length=100, default=url + 'campaigns', editable=False)
    templates = models.CharField(max_length=100, default=url + 'templates', editable=False)
    populations = models.CharField(max_length=100, default=url + 'populations', editable=False)
    suppressionLists = models.CharField(max_length=100, default=url + 'suppressionLists', editable=False)
    archives = models.CharField(max_length=100, default=url + 'archives', editable=False)
    key = models.CharField(max_length=100, editable=False)

    def save(self, *args, **kwargs):
        self.id = random.randint(100000000, 999999999)
        self.key = get_random_string(20)
        print(self.key)
        super(Client, self).save(*args, **kwargs)


class Types(models.TextChoices):
    EMAIL = 'EMAIL'
    LETTER = 'LETTER'
    TWILIO = 'TWILIO'


class Template(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=4000, blank=True)
    dynamic = models.BooleanField(blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=55), blank=True, null=True)
    content = models.CharField(max_length=100, blank=True)
    comments = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=7, choices=Types.choices)
    client = models.CharField(max_length=100, default=url + 'client', editable=False)
    url = models.CharField(max_length=100, default=url + 'templates/', editable=False)  ## not Dispatch just helper

    def save(self, *args, **kwargs):
        identifier = random.randint(100000000, 999999999)
        self.id = identifier
        self.url = self.url + str(identifier)
        super(Template, self).save(*args, **kwargs)


class Campaign(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    tags = ArrayField(models.CharField(max_length=55), blank=True, null=True)
    productionMode = models.BooleanField(default=True)  # Default to true for us
    communications = ArrayField(models.CharField(max_length=55), blank=True, null=True)
    client = models.CharField(max_length=100, default=url + 'client', editable=False)
    url = models.CharField(max_length=100, default=url + 'campaigns/', editable=False)  ## not Dispatch just helper

    def save(self, *args, **kwargs):
        self.url = self.url + str(self.id)  # todo: pretty sure we want this to be user defined. right now user value would be overwritten and we wouldn't know the id of the campaign
        super(Campaign, self).save(*args, **kwargs)


class Communication(models.Model):
    class AlertOnChoices(models.TextChoices):
        ERRORS = 'ERRORS'
        WARNINGS = 'WARNINGS'
        ALL = 'ALL'

    id = models.IntegerField(primary_key=True)  # will be stage id
    name = models.CharField(max_length=100)
    comments = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=6, choices=Types.choices)  # todo- if email then email must be defined
    email = models.JSONField(null=True)  # todo- how to validate/do we need to
    destinations = models.JSONField(null=True)  # todo- how to validate? do I need to validate? examine use cases
    alertOn = models.CharField(max_length=8, choices=AlertOnChoices.choices, default='ALL')
    placeholders = JSONField(blank=True, null=True)  # todo- how to validate/do we need to
    template = models.CharField(max_length=300, blank=True)
    adhocs = models.CharField(max_length=300, blank=True)
    notificationAddresses = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    campaign = models.CharField(max_length=300, blank=True)
    url = models.CharField(max_length=100, default=url + 'communications/', editable=False)  ## not Dispatch just helper

    def save(self, *args, **kwargs):
        if self.url[-1] == '/':
            self.url = self.url + str(self.id)
        super(Communication, self).save(*args, **kwargs)


class Population(models.Model):
    class DataSourceTypes(models.TextChoices):
        MANUALEMAILLIST = 'ManualEmailList'
        MANUALIDLIST = 'ManualIDList'
        MANUALECSVLIST = 'ManualCSVList'
        DATABASEQUERY = 'DatabaseQuery'
        WEBSERVICECALL = 'WebServiceCall'
        PREDEFINEDPOPULATION = 'PredefinedPopulation'
        ADHOCLIST = 'AdhocList'

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    dataSourceType = models.CharField(max_length=20, choices=DataSourceTypes.choices)
    description = models.CharField(max_length=4000, blank=True)
    parameterized = models.BooleanField(blank=True, null=True, default=False)
    archived = models.BooleanField(blank=True, null=True, default=False)
    hidden = models.BooleanField(blank=True, null=True, default=False)
    client = models.CharField(max_length=100, default=url + 'client', editable=False)
    tags = ArrayField(models.CharField(max_length=55), blank=True, null=True)
    manualEmailList = models.JSONField()
    url = models.CharField(max_length=100, default=url + 'populations/', editable=False)  ## not Dispatch just helper

    def save(self, *args, **kwargs):
        identifier = random.randint(100000000, 999999999)
        self.id = identifier
        self.url = self.url + str(identifier)
        super(Population, self).save(*args, **kwargs)


class Batch(models.Model):
    class StatusTypes(models.TextChoices):
        SCHEDULED = 'SCHEDULED'
        GENERATING = 'GENERATING'
        GENERATING_ADHOC = 'GENERATING_ADHOC'
        GENERATION_QUEUED = 'GENERATION_QUEUED'
        PENDING_APPROVAL = 'PENDING_APPROVAL'
        SEND_CONFIGURE = 'SEND_CONFIGURE'
        WAITING = 'WAITING'
        SENDING = 'SENDING'
        NO_MESSAGES = 'NO_MESSAGES'
        COMPLETED = 'COMPLETED'
        ERROR = 'ERROR'
        CANCELLED = 'CANCELLED'

    id = models.IntegerField(primary_key=True)
    runDate = models.DateTimeField()
    numMessages = models.IntegerField()
    numErrors = models.IntegerField()
    status = models.CharField(max_length=30, choices=StatusTypes.choices)
    communication = models.CharField(max_length=100, default=url + 'communications/', editable=False)
    members = ArrayField(models.JSONField(), blank=True, null=True)  # this may need tweaking
    url = models.CharField(max_length=300, default=url + 'batches/')

    def save(self, *args, **kwargs):
        identifier = random.randint(100000000, 999999999)
        self.id = identifier
        self.url = self.url + str(self.id)
        super(Batch, self).save(*args, **kwargs)

    def create_from_adhoc(self, members, communication_url):
        self.runDate = datetime.datetime.utcnow()
        self.numMessages = len(members)
        self.numErrors = 0
        self.status = "COMPLETED"
        self.communication = communication_url
        for member in members:
            member['id'] = str(random.randint(10 ** 9, 10 ** 10 - 1))
        self.members = members
        self.save()
        return self


# rough draft of Member model; might not need EVER
class Member(models.Model):
    toName = models.CharField(max_length=100)
    toAddress = models.EmailField(max_length=100)


class Message(models.Model):
    class Types(models.TextChoices):
        EMAIL = 'EMAIL'
        PRINT = 'PRINT'
        TWILIO = 'TWILIO'

    id = models.IntegerField(primary_key=True, editable=False)
    memberId = models.CharField(max_length=100)
    type = models.CharField(max_length=15, choices=Types.choices)
    excluded = models.BooleanField(default=False)
    member = models.JSONField()
    sentDate = models.DateTimeField(null=True)
    batch = models.JSONField()
    receiptDate = models.DateTimeField(null=True)
    fromName = models.CharField(max_length=100)
    fromAddress = models.EmailField(default="anemail@email.com")
    fromPhone = models.CharField(max_length=100, default='0000000')
    toAddress = models.EmailField()
    toName = models.CharField(max_length=100)
    toPhone = models.CharField(max_length=10, default='0000000')
    subject = models.CharField(max_length=100)
    url = models.CharField(max_length=300, default=url + 'messages/')

    def save(self, *args, **kwargs):
        identifier = random.randint(100000000, 999999999)
        self.id = identifier
        self.url = self.url + str(identifier)
        super(Message, self).save(*args, **kwargs)

    def create_from_adhoc(self, member, batch, communication):
        self.type = 'EMAIL'
        self.toAddress = member['toAddress']
        self.toName = member['toName']
        self.memberId = member['id']
        self.member = member
        self.sentDate = datetime.datetime.utcnow()
        self.batch = batch
        self.receiptDate = None
        self.fromAddress = communication.email['fromAddress']
        self.fromName = communication.email['fromName']
        self.subject = communication.email['subject']
        self.url = self.url + member['id']
        self.save()
        return self



