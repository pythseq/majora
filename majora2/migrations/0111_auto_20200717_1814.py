# Generated by Django 2.2.13 on 2020-07-17 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0110_auto_20200717_1811'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='majoradataview',
            options={'permissions': [('can_read_dataview_via_api', 'Can read the contents of data views via the API')]},
        ),
    ]