from django.contrib.auth.models import User
from django.test import TransactionTestCase
from django.urls import reverse

from bibliotech.models import ItemGroup, Checkout, Member
from bibliotech.misc_views import create_checkout


class CheckoutTests(TransactionTestCase):
    fixtures = ["test_fixtures.json"]

    def setUp(self):
        # Create a test user in the database
        self.user = User.objects.create(username="member", email="member@test.edu")
        self.user.set_password("password")
        self.user.save()
        # Create our proxy model
        self.member = Member.objects.create(user=self.user, member_id="000000")
        self.member.save()

    def test_good_create_checkout(self):
        """
        When an authenticated user hits the create_checkout endpoint, a checkout
        entry should be created for each item in the cart
        """
        cart = {"1": 1}  # ItemGroup w/ pk=1 is defined in test fixtures
        self.client.login(username="member", password="password")
        session = self.client.session
        session["cart"] = cart
        session.save()
        url = reverse("create-checkout")
        expected_url = reverse("success-view")  # Our expected redirect

        response = self.client.post(url, {"agreed": True}, follow=True)

        # Request should redirect to a success page
        self.assertRedirects(response, expected_url)

        # A checkout entry should be created in the database
        checkout = Checkout.objects.first()
        self.assertIsNotNone(checkout)

        session = response.client.session
        self.assertEqual(session["cart"], dict())

    def test_anon_user_checkouts(self):
        """
        Anonymous users should be redirected to a login page
        """
        url = reverse("checkout-list")

        response = self.client.get(url, follow=True)
        self.assertRedirects(response, reverse('login'))
