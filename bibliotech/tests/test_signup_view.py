from django.contrib.auth.models import User
from django.test import TransactionTestCase
from django.urls import reverse


class SignupTests(TransactionTestCase):
    def test_signup_form_errors(self):
        response = self.client.post(reverse("signup"))
        self.assertContains(response, "This field is required", count=6)

    def test_passwords_dont_match(self):
        response = self.client.post(
            reverse("signup"),
            {
                "fname": "Bob",
                "lname": "Smith",
                "username": "bobsmith",
                "email": "bobertsmith@test.com",
                "password": "password",
                "password_confirm": "password2",
            },
        )
        self.assertInHTML("Passwords don't match!", response.content.decode('utf-8'))

    def test_signup_flow(self):
        fields = {
            "fname": "Bob",
            "lname": "Smith",
            "email": "bobertsmith@test.com",
            "username": "bobsmith",
            "password": "password",
            "password_confirm": "password",
        }

        response = self.client.post(reverse("signup"), fields, follow=True)

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertEqual(User.objects.filter(username=fields["username"]).count(), 1)
