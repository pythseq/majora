# Generated by Django 2.2.10 on 2020-05-04 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0071_auto_20200504_1706'),
    ]

    operations = [
        migrations.RenameField(
            model_name='institute',
            old_name='gisaid_addr',
            new_name='gisaid_lab_addr',
        ),
        migrations.AddField(
            model_name='institute',
            name='gisaid_lab_name',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
