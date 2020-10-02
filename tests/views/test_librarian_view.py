from datetime import timedelta
from django.contrib.auth.models import User, Group
from django.test import TestCase, TransactionTestCase
from django.utils import timezone
from django.urls import reverse
from parameterized import parameterized

import equilizer.checkout_manager as checkout_manager
from equilizer.models import Checkout, Item
from equilizer.class_views.admin_views import LibrarianView


class LibrarianViewDataRetrieval(TestCase):
    fixtures = ["test_fixtures.json"***REMOVED***

    def setUp(self):
        # Create a test user
        self.user = User.objects.create(username="member", email="member@test.edu")
        self.user.set_password("password")
        self.user.save()

        # Create some checkouts
        due_date = timezone.now() + timedelta(5)
        past_checkout_date = timezone.now() + timedelta(-5)
        self.items = [Item.objects.get(pk=1), Item.objects.get(pk=2)***REMOVED***

        # Checkout 2 items on different dates
        checkout_manager.checkout_items(self.items[0***REMOVED***, due_date, self.user)
        checkout_manager.checkout_items(
            self.items[1***REMOVED***, due_date, self.user, checkout_date=past_checkout_date
        )

        # Checkout, then return an item
        c = checkout_manager.checkout_items(
            Item.objects.get(pk=4), due_date, self.user
        )[0***REMOVED***
        c.approval_status = "APPROVED"
        c.save()
        checkout_manager.return_items(c)

    def test_get_pending_checkouts(self):
        ***REMOVED***
        Assert that only pending checkouts are returned, and that they are sorted by
        date asc.
        ***REMOVED***
        view = LibrarianView()
        expected = Checkout.objects.filter(approval_status="PENDING").order_by(
            "checkout_date"
        )

        dto = view.get_pending_checkouts()

        self.assertEqual(list(dto), list(expected))
        # Checkout date of the first item should be before the next item
        self.assertLess(list(dto)[0***REMOVED***.checkout_date, list(dto)[1***REMOVED***.checkout_date)


class LibrarianViewAuthTests(TransactionTestCase):
    ***REMOVED***
    Library management endpoints should be accessible ONLY to users in librarian group.
    ***REMOVED***

    fixtures = ["test_fixtures.json"***REMOVED***

    def setUp(self):
        # Create the librarian group
        librarian_group = Group.objects.get_or_create(name="librarian")[0***REMOVED***

        # Normal user
        self.normal_user = User.objects.create(
            username="member", email="member@test.edu"
        )
        self.normal_user.set_password("password")
        self.normal_user.save()

        # Librarian user
        self.librarian = User.objects.create(
            username="librarian", email="librarian@test.edu"
        )
        self.librarian.set_password("password")
        self.librarian.groups.add(librarian_group)
        self.librarian.save()

        # Create a checkout request
        due_date = timezone.now() + timedelta(4)

        self.item_id = 1
        self.item = Item.objects.get(pk=self.item_id)

        # Select the first item since checkout manager returns a list
        self.checkout = checkout_manager.checkout_items(
            self.item,
            due_date,
            self.normal_user,
        ).pop()

        # Some other common variables
        self.deny_endpoint = reverse("deny-checkout", args=(self.checkout.id,))

    def test_authorized_approve_endpoint(self):
        ***REMOVED***
        Valid requests to /checkout/<int>/approve should approve the request and redirect to
        the control panel
        ***REMOVED***
        self.client.login(username="librarian", password="password")
        response = self.client.post(
            reverse("approve-checkout", args=(self.checkout.id,))
        )

        # Assert redirect
        self.assertRedirects(response, reverse("librarian-control-panel"))

        # Assert relevant objects are updated
        self.checkout.refresh_from_db()
        self.assertEqual(self.checkout.approval_status, "APPROVED")

    def test_unauthorized_approve_endpoint(self):
        ***REMOVED***
        Invalid requests to /checkout/<int>/approve should return 403 for an unauthorized user
        ***REMOVED***
        self.client.login(username="member", password="password")
        response = self.client.post(
            reverse("approve-checkout", args=(self.checkout.id,))
        )

        self.assertEqual(response.status_code, 403)

    @parameterized.expand(
        [
            ("librarian", "password", 200),
            ("member", "password", 403),
        ***REMOVED***
    )
    def test_authorized_deny_view(self, username, password, expected_status):
        ***REMOVED***
        Valid get request to /checkout/<int>/deny should return a view
        Invalid get request should return 403
        ***REMOVED***
        self.client.login(username=username, password=password)
        response = self.client.get(self.deny_endpoint)
        self.assertEqual(response.status_code, expected_status)

    @parameterized.expand(
        [
            ("librarian", "password", 200),
            ("member", "password", 403),
        ***REMOVED***
    )
    def test_authorized_deny_post(self, username, password, expected_status):
        ***REMOVED***
        Valid request should redirect to control panel
        Non-librarian users should have 403 returned.
        ***REMOVED***
        self.client.login(username=username, password=password)

        # Mimick a post request with data
        response = self.client.post(
            self.deny_endpoint, {"reason": "reason"***REMOVED***, follow=True
        )
        self.assertEqual(response.status_code, expected_status)

        # If we get a redirect as our status code, assert that we're redirect to the control panel
        if expected_status == 302:
            self.assertRedirects(reverse("librarian-control-panel"))

    def test_authorized_deny_post_blank_reason(self):
        self.client.login(username="librarian", password="password")

        response = self.client.post(self.deny_endpoint, {"reason": ""***REMOVED***, follow=True)
        self.assertContains(response, "This field is required")
