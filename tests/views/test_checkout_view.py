from django.contrib.auth.models import User
from django.test import TransactionTestCase
from django.urls import reverse

from equilizer.models import ItemGroup, Checkout, Member
from equilizer.views import create_checkout


class CheckoutTests(TransactionTestCase):
    fixtures = ["test_fixtures.json"***REMOVED***

    def setUp(self):
        # Create a test user in the database
        self.user = User.objects.create(username="member", email="member@test.edu")
        self.user.set_password("password")
        self.user.save()
        # Create our proxy model
        self.member = Member.objects.create(user=self.user, member_id="000000")
        self.member.save()

    def test_good_create_checkout(self):
        ***REMOVED***
        When an authenticated user hits the create_checkout endpoint, a checkout
        entry should be created for each item in the cart
        ***REMOVED***
        cart = {"1": 1***REMOVED***  # ItemGroup w/ pk=1 is defined in test fixtures
        self.client.login(username="member", password="password")
        session = self.client.session
        session["cart"***REMOVED*** = cart
        session.save()
        url = reverse("create-checkout")
        expected_url = reverse("success-view")  # Our expected redirect

        response = self.client.post(url, follow=True)

        # Request should redirect to a success page
        self.assertRedirects(response, expected_url)

        # A checkout entry should be created in the database
        checkout = Checkout.objects.first()
        self.assertIsNotNone(checkout)

    def test_anon_user_checkouts(self):
        ***REMOVED***
        Anonymous users should be redirected to a login page
        ***REMOVED***
        url = reverse("checkout-list")

        response = self.client.get(url, follow=True)
        self.assertRedirects(response, reverse('login'))
