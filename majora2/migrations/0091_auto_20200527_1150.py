# Generated by Django 2.2.10 on 2020-05-27 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0090_auto_20200526_1307'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'permissions': [('can_approve_profiles', 'Can approve new user profiles for their organisation')]},
        ),
    ]
