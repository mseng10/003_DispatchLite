from django.db import models
import random
from django.utils.crypto import get_random_string
import os

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