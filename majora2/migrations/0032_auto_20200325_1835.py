# Generated by Django 2.2.10 on 2020-03-25 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0031_auto_20200325_1834'),
    ]

    operations = [
        migrations.RenameField(
            model_name='biosampleartifact',
            old_name='specimen_type',
            new_name='sample_type_curent',
        ),
    ]
