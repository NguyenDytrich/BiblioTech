from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TransactionTestCase


class LoginViewTests(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create(username="member", email="member@test.edu")
        self.user.set_password("password")
        self.user.save()

    def test_login_flow_with_registered_user(self):
        credentials = {"username": "member", "password": "password"}
        response = self.client.post(reverse("login"), credentials, follow=True)
        self.assertIn("user", response.context)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_redirect_when_not_anon(self):
        self.client.login(username="member", password="password")
        response = self.client.get(reverse("login"), follow=True)
        self.assertRedirects(response, reverse("itemgroup-list"))

    def test_returns_errors_no_user(self):
        credentials = { "username": "doesnotexist", "password": "password" }
        response = self.client.post(reverse("login"), credentials, follow=True)
        self.assertContains(response, "Invalid username or password", count=1)

    def test_returns_errors_wrong_password(self):
        credentials = { "username": "member", "password": "wrong_password" }
        response = self.client.post(reverse("login"), credentials, follow=True)
        self.assertContains(response, "Invalid username or password", count=1)
