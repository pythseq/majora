# Generated by Django 2.2.10 on 2020-03-22 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0021_auto_20200322_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biosampleartifact',
            name='root_sample_id',
            field=models.CharField(blank=True, max_length=48, null=True),
        ),
        migrations.AlterField(
            model_name='biosampleartifact',
            name='sender_sample_id',
            field=models.CharField(blank=True, max_length=48, null=True),
        ),
    ]
