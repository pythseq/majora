import datetime
import uuid

from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from django_otp import DEVICE_ID_SESSION_KEY
from django_otp.plugins.otp_static.models import StaticDevice

from majora2 import models

class BasicAPITest(TestCase):
    def setUp(self):
        self.c = Client()

        # Create an institute and user profile
        hoot = models.Institute(code="HOOT", name="Hypothetical University of Hooting")
        hoot.save()

        # Create a fully approved profile user
        user = User.objects.create(username='api_user', email='api@example.org')
        user.set_password('password')
        user.is_active = True # sysadmins mark this field
        user.save()
        profile = models.Profile(user=user, institute=hoot, is_site_approved=True)
        profile.save()

        self.user = user

        # Create an API key def
        kd = models.ProfileAPIKeyDefinition(
                                            key_name = "Kipper's Magic Key",
                                            lifespan = datetime.timedelta(days=7),
                                            is_service_key=False,
                                            is_read_key=False,
                                            is_write_key=False,
        )
        kd.save()
        self.kd = kd

        # Give the user a key: use the client and just post a request to the key activator
        # Log the user in and mock an OTP (https://github.com/Bouke/django-two-factor-auth/issues/244)
        self.c.login(username='api_user', password='password')
        device = StaticDevice.objects.get_or_create(user=user)[0]
        device.save()
        session = self.c.session
        session[DEVICE_ID_SESSION_KEY] = device.persistent_id
        session.save()
        response = self.c.post(reverse('api_keys_activate'), {'key_name': self.kd.key_name}, secure=True)
        self.key = self.user.profile.get_generated_api_keys()[0]

    def test_biosample_bad_json_content_type(self):
        payload = {
            "username": self.user.username,
            "token": self.key.key,
            "client_name": "pytest",
            "client_version": 1,
        }
        response = self.c.post(reverse('api.artifact.biosample.add'), payload, secure=True)
        self.assertEqual(400, response.status_code)

    def test_biosample_bad_json_no_username(self):
        payload = {
            "token": self.key.key,
            "client_name": "pytest",
            "client_version": 1,
        }
        response = self.c.post(reverse('api.artifact.biosample.add'), payload, secure=True, content_type="application/json")
        self.assertEqual(400, response.status_code)

    def test_biosample_bad_json_bad_key(self):
        payload = {
            "username": self.user.username,
            "token": uuid.uuid4(),
            "client_name": "pytest",
            "client_version": 1,
        }
        response = self.c.post(reverse('api.artifact.biosample.add'), payload, secure=True, content_type="application/json")
        self.assertEqual(400, response.status_code)

    def test_biosample_bad_json_revoked_key(self):
        self.key.was_revoked = True
        self.key.save()

        payload = {
            "username": self.user.username,
            "token": self.key.key,
            "client_name": "pytest",
            "client_version": 1,
        }
        response = self.c.post(reverse('api.artifact.biosample.add'), payload, secure=True, content_type="application/json")
        self.assertEqual(400, response.status_code)

        self.key.is_revoked = False
        self.key.save()

    def test_biosample_bad_json_early_key(self):
        v = self.key.validity_start
        self.key.validity_start = datetime.datetime.now() + datetime.timedelta(minutes=10) # key valid in 10mins
        self.key.save()

        payload = {
            "username": self.user.username,
            "token": self.key.key,
            "client_name": "pytest",
            "client_version": 1,
        }
        response = self.c.post(reverse('api.artifact.biosample.add'), payload, secure=True, content_type="application/json")
        self.assertEqual(400, response.status_code)

        self.key.validity_start = v
        self.key.save()

    def test_biosample_bad_json_late_key(self):
        v = self.key.validity_end
        self.key.validity_end = datetime.datetime.now() - datetime.timedelta(minutes=10) # key expired 10mins ago
        self.key.save()

        payload = {
            "username": self.user.username,
            "token": self.key.key,
            "client_name": "pytest",
            "client_version": 1,
        }
        response = self.c.post(reverse('api.artifact.biosample.add'), payload, secure=True, content_type="application/json")
        self.assertEqual(400, response.status_code)

        self.key.validity_end = v
        self.key.save()


    def test_biosample_add(self):
        payload = {
            "username": self.user.username,
            "token": self.key.key,
            "biosamples": [
                {
                    "adm1": "UK-ENG",
                    "adm2": "BIRMINGHAM",
                    "central_sample_id": "HOOT-00001",
                    "collection_date": "2020-08-24",
                    "is_surveillance": False,
                },
            ],
            "client_name": "pytest",
            "client_version": 1,
        }
        response = self.c.post(reverse('api.artifact.biosample.add'), payload, secure=True, content_type="application/json")
        self.assertEqual(200, response.status_code)

        self.assertEqual(1, models.BiosampleArtifact.objects.count())

        bs = models.BiosampleArtifact.objects.all()[0]
        self.assertEqual(payload["biosamples"][0]["central_sample_id"], bs.dice_name)

