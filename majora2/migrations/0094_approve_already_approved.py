# Generated by Django 2.2.10 on 2020-05-27 13:10

from django.db import migrations

def approve_approved(apps, schema_editor):
    Profile = apps.get_model("majora2", "Profile")
    for profile in Profile.objects.all():
        if profile.user.is_active:
            profile.is_site_approved = True
            profile.save()

class Migration(migrations.Migration):

    dependencies = [
        ('majora2', '0093_profile_is_site_approved'),
    ]

    operations = [
        migrations.RunPython(approve_approved),
    ]
