from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from bibliotech.forms import UpdatePasswordForm


class UpdatePasswordFormTests(TestCase):
    def setUp(self):
        # Create a user to test with
        self.user = User.objects.create(username="member", email="member@test.edu")
        self.user.set_password("password")
        self.user.save()

    def test_bad_password(self):
        fields = {
            "user_id": self.user.id,
            "password": "badpassword",
            "new_password": "newpassword",
            "new_confirmed": "newpassword",
        }

        expected_error = ValidationError(_("Incorrect password"))

        form = UpdatePasswordForm(fields)
        self.assertFalse(form.is_valid())
        self.assertIn("Incorrect password", form.errors.as_data().get("password")[0].messages)

    def test_mismatched_confirmation(self):
        fields = {
            "user_id": self.user.id,
            "password": "password",
            "new_password": "newpassword",
            "new_confirmed": "notthesame",
        }

        form = UpdatePasswordForm(fields)
        self.assertFalse(form.is_valid())
        self.assertIn("Passwords don't match!", form.errors.as_data().get("new_confirmed")[0].messages)
