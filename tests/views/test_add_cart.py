from django.contrib.auth.models import User
from django.contrib import messages
from django.test import TransactionTestCase
from django.urls import reverse

from equilizer.models import ItemGroup
from equilizer.views import add_to_cart


class CartTests(TransactionTestCase):
    fixtures = ["test_fixtures.json"***REMOVED***

    def setUp(self):
        self.user = User.objects.create(username="member", email="member@test.edu")
        self.user.set_password("password")
        self.user.save()

    def test_add_cart_flow_with_registered_user(self):
        self.client.login(username="member", password="password")
        url = reverse("cart-add", args=(1,))
        redirect_url = reverse("itemgroup-detail", args=(1,))
        response = self.client.post(url, follow=True)

        self.assertEqual(self.client.session["cart"***REMOVED***, {"1": 1***REMOVED***)
        self.assertEqual(self.client.session["cart_sum"***REMOVED***, 1)
        self.assertRedirects(response, redirect_url)

    def test_add_cart_flow_with_anon_user(self):
        response = self.client.post(
            reverse("cart-add", args=(1,)),
            follow=True,
        )
        redirect_url = reverse("itemgroup-detail", args=(1,))

        self.assertRedirects(response, f"{reverse('login')***REMOVED***?next=%2Fcart%2Fadd%2F1")

        credentials = {
            "username": "member",
            "password": "password",
            "next": "/cart/add/1",
    ***REMOVED***
        response = self.client.post(f'{reverse("login")***REMOVED***', credentials, follow=True)
        self.assertRedirects(response, redirect_url)

    def test_add_cart_flow_multiple_same_item(self):
        self.client.login(username="member", password="password")
        url = reverse("cart-add", args=(3,))
        redirect_url = reverse("itemgroup-detail", args=(3,))

        response = self.client.post(url)
        response = self.client.post(url)

        self.assertEqual(self.client.session["cart"***REMOVED***, {"3": 2***REMOVED***)
        self.assertEqual(self.client.session["cart_sum"***REMOVED***, 2)

    def test_add_cart_flow_quick_add_good_user(self):
        self.client.login(username="member", password="password")
        url = reverse("cart-add", args=(1,))
        redirect_url = reverse("itemgroup-list")

        response = self.client.post(url, {"return": redirect_url***REMOVED***, follow=True)

        self.assertRedirects(response, redirect_url)

    def test_add_cart_flow_max_items(self):
        ***REMOVED***
        If an add-to-cart request would exceed the number of available items,
        the view should redirect with an error message
        ***REMOVED***
        item_id = (1,)  # Assign this tuple for readability to pass as args
        url = reverse("cart-add", args=item_id)
        redirect_url = reverse("itemgroup-detail", args=item_id)
        expected_msg = "All available items are already in your cart!"

        # Login a user
        self.client.login(username="member", password="password")

        # Set our cart to have an item
        session = self.client.session
        session["cart"***REMOVED*** = {"1": 1***REMOVED***
        session.save()

        # Make the request
        response = self.client.post(url, follow=True)

        # Get the messages, then create a list of their string representations
        # We need to get the messages in this way since we're using FallbackStorage
        # and the redirect is contextless
        msgs = list(messages.get_messages(response.wsgi_request))
        str_msgs = [str(m) for m in msgs***REMOVED***

        # The POST request should add a message
        self.assertIn(expected_msg, str_msgs)
        # Our view should redirect us to the item page
        self.assertRedirects(response, redirect_url)
        # The message should be rendered in the DOM
        self.assertContains(response, expected_msg)
