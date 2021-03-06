import django.dispatch
new_registration = django.dispatch.Signal(providing_args=["username", "first_name", "last_name", "organisation", "email"])
site_approved_registration = django.dispatch.Signal(providing_args=["approver", "approved_profile"])
activated_registration = django.dispatch.Signal(providing_args=["username", "email"])
new_sample = django.dispatch.Signal(providing_args=["sample_id", "submitter"])
