from datetime import timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from equilizer.models import Checkout, Item
from parameterized import parameterized
import equilizer.checkout_manager as manager

class CheckoutTestCase(TestCase):
    fixtures = ["test_fixtures.json"***REMOVED***
    due_date = timezone.now() + timedelta(4)

    def test_good_checkout(self):
        ***REMOVED***
        Test a perfectly good checkout entry.
        ***REMOVED***
        item = Item.objects.get(pk=1)
        checkout = Checkout.objects.create(due_date=self.due_date)

        checkout.items.add(item)
        checkout.save()

        # Check default values
        self.assertEqual("PENDING", checkout.approval_status)
        self.assertEqual("OUTSTANDING", checkout.checkout_status)

        # Check the item is referenced
        self.assertEqual(item, checkout.items.all()[0***REMOVED***)


class CheckoutManagerTestCase(TestCase):
    fixtures = ["test_fixtures.json"***REMOVED***

    # Set a due date 4 days from now
    due_date = timezone.now() + timedelta(4)

    def test_good_checkout(self):
        item = Item.objects.get(pk=1)

        manager.checkout_items(item, self.due_date)

        # Check the that the item availability is set correctly
        self.assertEqual(item.availability, "CHECKED_OUT")

    def test_good_checkout_multiple_items(self):
        items = Item.objects.all()
        manager.checkout_items(items, self.due_date)

        # Iterator executes the query, so we're not looking into the cache.
        for item in items.iterator():
            self.assertEqual(item.availability, "CHECKED_OUT")

    def test_good_checkout_with_different_checkout_date(self):
        items = Item.objects.all()
        checkout_date = self.due_date + timedelta(-2)
        manager.checkout_items(items, self.due_date, checkout_date=checkout_date)

        self.assertEqual(
            Checkout.objects.get(pk=1).checkout_date, checkout_date
        )

    @parameterized.expand(["UNAVAILABLE", "HOLD", "CHECKED_OUT", "LOST"***REMOVED***)
    def test_bad_checkout_item_unavailable(self, avail):
        ***REMOVED***
        Test that any non-available item throws an error
        ***REMOVED***
        item = Item.objects.get(pk=1)
        # Oh no, the item we want isn't available
        item.availability = avail
        item.save()

        items = Item.objects.all()

        with self.assertRaises(ValidationError):
            manager.checkout_items(items, self.due_date)

    def test_bad_checkout_date(self):
        ***REMOVED***
        Test that the checkout date must be before the due date
        ***REMOVED***
        items = Item.objects.all()
        # use the class's due_date variable which is a time in the future
        checkout_date = self.due_date
        due_date = timezone.now()

        with self.assertRaises(ValidationError):
            manager.checkout_items(items, due_date, checkout_date=checkout_date)
