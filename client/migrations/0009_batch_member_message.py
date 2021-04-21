# Generated by Django 3.1.5 on 2021-04-13 23:10

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_population_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('runDate', models.DateTimeField()),
                ('numMessages', models.IntegerField()),
                ('numErrors', models.IntegerField()),
                ('status', models.CharField(choices=[('SCHEDULED', 'Scheduled'), ('GENERATING', 'Generating'), ('GENERATING_ADHOC', 'Generating Adhoc'), ('GENERATION_QUEUED', 'Generation Queued'), ('PENDING_APPROVAL', 'Pending Approval'), ('SEND_CONFIGURE', 'Send Configure'), ('WAITING', 'Waiting'), ('SENDING', 'Sending'), ('NO_MESSAGES', 'No Messages'), ('COMPLETED', 'Completed'), ('ERROR', 'Error'), ('CANCELLED', 'Cancelled')], max_length=30)),
                ('communication', models.CharField(default='http://127.0.0.1:8000/communications/', editable=False, max_length=100)),
                ('members', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), blank=True, null=True, size=None)),
                ('url', models.CharField(default='http://127.0.0.1:8000/batches/', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toName', models.CharField(max_length=100)),
                ('toAddress', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('memberId', models.CharField(editable=False, max_length=100)),
                ('type', models.CharField(choices=[('EMAIL', 'Email'), ('PRINT', 'Print'), ('TWILIO', 'Twilio')], max_length=15)),
                ('excluded', models.BooleanField(default=False)),
                ('member', models.JSONField()),
                ('sentDate', models.DateTimeField(null=True)),
                ('batch', models.JSONField()),
                ('receiptDate', models.DateTimeField()),
                ('fromName', models.CharField(max_length=100)),
                ('fromAddress', models.EmailField(default='anemail@email.com', max_length=254)),
                ('fromPhone', models.CharField(default='0000000', max_length=100)),
                ('toAddress', models.EmailField(max_length=254)),
                ('toName', models.CharField(max_length=100)),
                ('toPhone', models.CharField(default='0000000', max_length=10)),
                ('subject', models.CharField(max_length=100)),
            ],
        ),
    ]
