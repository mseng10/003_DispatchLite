# Generated by Django 3.1.5 on 2021-04-09 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='archives',
            field=models.CharField(default='http://127.0.0.1:8000/archives', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='campaigns',
            field=models.CharField(default='http://127.0.0.1:8000/campaigns', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='populations',
            field=models.CharField(default='http://127.0.0.1:8000/populations', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='suppressionLists',
            field=models.CharField(default='http://127.0.0.1:8000/suppressionLists', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='templates',
            field=models.CharField(default='http://127.0.0.1:8000/templates', editable=False, max_length=100),
        ),
    ]