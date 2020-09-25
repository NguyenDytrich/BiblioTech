from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase


class LoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="member", email="member@test.edu")
        self.user.set_password("password")
        self.user.save()

    def test_login_flow_with_registered_user(self):
        credentials = {"username": "member", "password": "password"***REMOVED***
        response = self.client.post(reverse("login"), credentials, follow=True)
        self.assertIn("user", response.context)
        self.assertTrue(response.context["user"***REMOVED***.is_authenticated)
