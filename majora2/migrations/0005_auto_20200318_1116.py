# Generated by Django 2.2.10 on 2020-03-18 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0004_make_ins'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='organisation',
        ),
        migrations.AddField(
            model_name='biosourcesamplingprocess',
            name='collection_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='majora2.Institute'),
        ),
    ]
