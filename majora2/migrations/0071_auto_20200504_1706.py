# Generated by Django 2.2.10 on 2020-05-04 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0070_publishedartifactgroup_public_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='gisaid_addr',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='institute',
            name='gisaid_list',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='institute',
            name='gisaid_mail',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='institute',
            name='gisaid_user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
