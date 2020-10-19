from django.contrib.auth.models import User
from django.test import TransactionTestCase
from django.urls import reverse


class SignupTests(TransactionTestCase):
    def test_signup_form_errors(self):
        response = self.client.post(reverse("signup"))
        self.assertContains(response, "This field is required", count=7)

    def test_passwords_dont_match(self):
        response = self.client.post(
            reverse("signup"),
            {
                "fname": "Bob",
                "lname": "Smith",
                "username": "bobsmith",
                "student_id": "123456",
                "email": "bobertsmith@test.com",
                "password": "asfeh52389",
                "password_confirm": "pasfeh52389assword2",
            },
        )
        self.assertInHTML("Passwords don't match!", response.content.decode('utf-8'))

    def test_signup_flow(self):
        fields = {
            "fname": "Bob",
            "lname": "Smith",
            "email": "bobertsmith@test.com",
            "student_id": "123456",
            "username": "bobsmith",
            "password": "passwordasfeh52389",
            "password_confirm": "passwordasfeh52389",
        }

        response = self.client.post(reverse("signup"), fields, follow=True)

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertEqual(User.objects.filter(username=fields["username"]).count(), 1)

class SignupFlowTest(TransactionTestCase):

    def test_profile_view_renders_for_new_user(self):
        fields = {
            "fname": "Bob",
            "lname": "Smith",
            "email": "bobertsmith@test.com",
            "student_id": "123456",
            "username": "bobsmith",
            "password": "passwordasfeh52389",
            "password_confirm": "passwordasfeh52389",
        }

        # User signs up
        self.client.post(reverse("signup"), fields)

        # Mimick our user logging in
        self.client.login(username="bobsmith", password="passwordasfeh52389")

        # User navigates to their profile page
        response = self.client.get(reverse("user-profile"))

        # Status code should be 200
        self.assertEqual(response.status_code, 200)

        # Their student_id should be visible on their profile
        self.assertContains(response, fields["student_id"])
