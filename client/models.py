from django.db import models
import random
from django.utils.crypto import get_random_string
import os
from django.contrib.postgres.fields import ArrayField, JSONField

if 'WEBSITE_HOSTNAME' in os.environ:
    url = 'finalurl'
else:
    url = 'http://127.0.0.1:8000/'


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


class Template(models.Model):
    class Types(models.TextChoices):
        EMAIL = 'EMAIL'
        LETTER = 'LETTER'
        TWIML = 'TWIML'

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
        identifier = random.randint(100000000, 999999999)
        self.id = identifier
        self.url = self.url + str(identifier)
        super(Campaign, self).save(*args, **kwargs)


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


# rough draft of Batch model
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
    communication = models.CharField(max_length=100, default=url + 'communication', editable=False)
    members = ArrayField(models.CharField(max_length=55), blank=True,
                         null=True)  # this needs tweaking --> maybe instead of charField we should use json field

    def save(self, *args, **kwargs):
        identifier = random.randint(100000000, 999999999)
        self.id = identifier
        self.url = self.url + str(identifier)
        super(Batch, self).save(*args, **kwargs)


# rough draft of Member model
class Member(models.Model):
    toName = models.CharField()
    toAddress = models.EmailField()

