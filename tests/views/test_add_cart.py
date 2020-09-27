from django.contrib.auth.models import User
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
