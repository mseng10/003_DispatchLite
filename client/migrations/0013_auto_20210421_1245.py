# Generated by Django 3.1.5 on 2021-04-21 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0012_merge_20210420_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='receiptDate',
            field=models.DateTimeField(null=True),
        ),
    ]