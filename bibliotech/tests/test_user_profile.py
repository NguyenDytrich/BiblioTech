from django.contrib.auth.models import User
from django.test import TransactionTestCase
from django.urls import reverse
from parameterized import parameterized

from library.models import Member


class UserProfileTests(TransactionTestCase):
    """
    Users should be able to see all their profile information
    """

    def setUp(self):
        # Create a user
        self.user = User.objects.create(username="member", email="member@test.edu")
        self.user.set_password("password")
        self.user.first_name = "Indigo"
        self.user.last_name = "Magenta"
        self.user.save()

        # Create a member profile for the user
        self.member = Member.objects.create(user=self.user, member_id="123456")
        self.member.save()

        # Create an auxilary user
        aux = User.objects.create(username="member2", email="member2@test.edu")
        aux.set_password("password")
        aux.save()
        aux_member = Member.objects.create(user=aux, member_id="123457")
        aux_member.save()

    def test_information_in_view(self):
        """
        User information should be visible to the user in the rendered html
        """
        self.client.login(username="member", password="password")

        response = self.client.get(reverse("user-profile"))

        self.assertContains(response, self.user.get_full_name())
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.member.member_id)

    @parameterized.expand(
        [
            ("member", "password"),
            ("member2", "password"),
        ]
    )
    def test_profile_context(self, username, password):
        """
        The profile context should contain the user's information
        """
        self.client.login(username=username, password=password)

        response = self.client.get(reverse("user-profile"))
        profile = response.context.get("profile")
        self.assertTrue(profile)
        self.assertEqual(profile.user.username, username)

    def test_profile_redirects_anon_user(self):
        """
        If an anon user makes a request to the user profile, should redirect to login
        """
        response = self.client.get(reverse("user-profile"))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('user-profile')}"
        )

    @parameterized.expand(
        [
            (
                "Valid (Don Juan)",
                {"email": "new@email.com", "fname": "Don", "lname": "Juan"},
                200,
            )
        ]
    )
    def test_update_profile(self, name, fields, expected):
        """
        Post request to the update-profile should update a specified field
        """
        self.client.login(username="member", password="password")

        response = self.client.post(reverse("user-profile-update"), fields)

        self.assertEqual(response.status_code, expected)

        self.user.refresh_from_db()
        if fields.get("email"):
            self.assertEqual(user.email, fields["email"])
        if fields.get("fname"):
            self.assertEqual(user.first_name, fields["fname"])
        if fields.get("lname"):
            self.assertEQual(user.last_name, fields["lname"])

    @parameterized.expand(
        [
            (
                "Valid password change",
                {
                    "password": "password",
                    "new_password": "password2",
                    "new_confirmed": "password2",
                },
                200,
            )
        ]
    )
    def test_change_password(self, name, fields, expected_status):
        self.client.login(username="member", password=fields["password"])

        fields["user_id"] = self.user.id
        response = self.client.post(reverse("user-change-password"), fields)

        user = User.objects.get(username="member")
        self.assertTrue(user.check_password(fields["new_password"]))

    def test_change_password_wrong_user(self):
        """
        A user should not be able to make a request to change another user's password
        """
        self.client.login(username="member2", password="password")

        fields = {
            "user_id": 1,
            "password": "password",
            "new_password": "password2",
            "new_confirmed": "password2",
        }

        response = self.client.post(reverse("user-profile-update"), fields)

        self.assertEqual(response.status_code, 403)
