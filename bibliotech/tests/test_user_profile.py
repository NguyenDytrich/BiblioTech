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


    def test_information_in_view(self):
        """
        User information should be visible to the user in the rendered html
        """
        self.client.login(username="member", password="password")

        # User profiles should be able to be accessed via username
        response = self.client.get(reverse("user-profile"), args=("member",))

        self.assertContains(response, self.user.get_full_name())
        self.assertContains(response, self.user.email())
        self.assertContains(response, self.member.member_id())

    def test_profile_url(self):
        self.client.login(username="member", password="password")

        # User profiles should be able to be accessed via username
        username = self.client.get(reverse("user-profile"), args=("member",))

        # User profiles should be able to be accessed via user ID
        user_id = self.client.get(reverse("user-profile"), args=(self.user.id,))

        self.assertEqual(username.response_code, 200)
        self.assertEqual(user_id.response_code, 200)


    @parameterized.expand([
        ("owner", "member", "password", 200),
        ("owner", "member2", "password", 403)
        ])
    def test_profile_private(self, name, username, password, status_code):
        """
        User profiles should be visible only to the logged-in user
        """
        self.client.login(username=username, password=password)
        response = self.client.get(reverse("user-profile"), args=(username,))
        self.assertEqual(response.status_code, status_code)

    def test_profile_not_accessible_by_anon_user(self):
        """
        If an anon user makes a request to the user profile, should return HTTP 403
        """
        response = self.client.get(reverse("user-profile"), args=(1,))
        self.assertEqual(response.status_code, 403)
