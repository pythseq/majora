# Generated by Django 2.2.10 on 2020-05-06 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0076_profileapikey_profileapikeydefinition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileapikey',
            name='validity_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profileapikey',
            name='validity_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profileapikeydefinition',
            name='key_name',
            field=models.CharField(max_length=48, unique=True),
        ),
    ]
