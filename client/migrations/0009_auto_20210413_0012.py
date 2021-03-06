# Generated by Django 3.1.5 on 2021-04-13 05:12

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_population_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='type',
            field=models.CharField(choices=[('EMAIL', 'Email'), ('LETTER', 'Letter'), ('TWILIO', 'Twilio')], max_length=7),
        ),
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('comments', models.CharField(blank=True, max_length=100)),
                ('type', models.CharField(choices=[('EMAIL', 'Email'), ('LETTER', 'Letter'), ('TWILIO', 'Twilio')], max_length=6)),
                ('alertOn', models.CharField(choices=[('ERRORS', 'Errors'), ('WARNINGS', 'Warnings'), ('ALL', 'All')], default='ALL', max_length=8)),
                ('template', models.CharField(blank=True, max_length=300)),
                ('adhocs', models.CharField(blank=True, max_length=300)),
                ('notificationAddresses', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.campaign')),
            ],
        ),
    ]
