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


    @parameterized.expand([
        ("member", "password"),
        ("member2", "password"),
        ])
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
        If an anon user makes a request to the user profile, should return HTTP 403
        """
        response = self.client.get(reverse("user-profile"))
        self.assertRedirects(response, reverse("login"))
