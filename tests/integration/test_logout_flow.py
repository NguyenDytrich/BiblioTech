from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TransactionTestCase

class LogoutTests(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create(username="member", email="member@test.edu")
        self.user.set_password("password")
        self.user.save()

    def test_good_logout(self):
        self.client.login(username="member", password="password")
        response = self.client.post(reverse("logout"), follow=True)
        self.assertFalse(response.context["user"].is_authenticated)
