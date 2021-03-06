# Generated by Django 2.2.10 on 2020-04-25 14:44

from django.db import migrations

def dra_path(apps, schema_editor):
    DigitalResourceArtifact = apps.get_model("majora2", "DigitalResourceArtifact")
    for dra in DigitalResourceArtifact.objects.all():
        if dra.primary_group:
            s = dra.primary_group.path + '/' + dra.current_name
            try:
                return s.split(":/")[1]
            except:
                return s
        else:
            return dra.current_name
        dra.current_path = s
        dra.save()

class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0059_digitalresourceartifact_current_path'),
    ]

    operations = [
        migrations.RunPython(dra_path),
    ]
