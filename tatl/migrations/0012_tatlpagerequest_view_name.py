# Generated by Django 2.2.13 on 2020-08-22 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tatl', '0011_tatlpagerequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='tatlpagerequest',
            name='view_name',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]