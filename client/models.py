from django.db import models
import random
from django.utils.crypto import get_random_string
import os
from django.contrib.postgres.fields import ArrayField,JSONField

if 'WEBSITE_HOSTNAME' in os.environ:
    url = 'finalurl'
else:
    url = 'http://127.0.0.1:8000/'

# Create your models here.
class Client(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    campaigns = models.CharField(max_length=100, default=url+'campaigns', editable=False)
    templates = models.CharField(max_length=100, default=url+'templates', editable=False)
    populations = models.CharField(max_length=100, default=url+'populations', editable=False)
    suppressionLists = models.CharField(max_length=100, default=url+'suppressionLists', editable=False)
    archives = models.CharField(max_length=100, default=url+'archives', editable=False)
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
    tags = ArrayField(models.CharField(max_length=55),blank=True,null=True)
    content = models.CharField(max_length=100, blank=True)
    comments = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=7, choices=Types.choices)
    client = models.CharField(max_length=100, default=url+'client', editable=False)
    url = models.CharField(max_length=100, default=url+'templates/', editable=False) ## not Dispatch just helper

    def save(self, *args, **kwargs):
        identifier = random.randint(100000000, 999999999)
        self.id = identifier
        self.url = self.url + str(identifier)
        super(Template, self).save(*args, **kwargs)

class Campaign(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    tags = ArrayField(models.CharField(max_length=55),blank=True,null=True)
    productionMode = models.BooleanField(default=True) # Default to true for us
    communications = ArrayField(models.CharField(max_length=55),blank=True,null=True)
    client = models.CharField(max_length=100, default=url+'client', editable=False)
    url = models.CharField(max_length=100, default=url+'campaigns/', editable=False) ## not Dispatch just helper

    def save(self, *args, **kwargs):
        identifier = random.randint(100000000, 999999999)
        self.id = identifier
        self.url = self.url + str(identifier)  # todo: pretty sure we want this to be user defined. right now user value would be overwritten and we wouldn't know the id of the campaign
        super(Campaign, self).save(*args, **kwargs)


class Communication(models.Model):
    class AlertOnChoices(models.TextChoices):
        ERRORS = 'ERRORS'
        WARNINGS = 'WARNINGS'
        ALL = 'ALL'

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    comments = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=6, choices=Types.choices)
    # email = None  # todo
    # destinations = None  # todo
    alertOn = models.CharField(max_length=8, choices=AlertOnChoices.choices, default='ALL')
    # placeholders = None  # todo
    template = models.CharField(max_length=300, blank=True)
    adhocs = models.CharField(max_length=300, blank=True)
    notificationAddresses = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)  # todo: pretty sure this is unneeded

    def save(self, *args, **kwargs):
        identifier = random.randint(100000000, 999999999)
        self.id = identifier  # todo: pretty sure we don't want this
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
    client = models.CharField(max_length=100, default=url+'client', editable=False)
    tags = ArrayField(models.CharField(max_length=55),blank=True,null=True)
    manualEmailList = models.JSONField()
    url = models.CharField(max_length=100, default=url+'populations/', editable=False) ## not Dispatch just helper

    def save(self, *args, **kwargs):
        identifier = random.randint(100000000, 999999999)
        self.id = identifier
        self.url = self.url + str(identifier)
        super(Population, self).save(*args, **kwargs)
