from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

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
