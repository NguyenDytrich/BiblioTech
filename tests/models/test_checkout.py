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
        checkout = Checkout.objects.create(due_date=self.due_date, item=item)

        checkout.save()

        # Check default values
        self.assertEqual("PENDING", checkout.approval_status)
        self.assertEqual("OUTSTANDING", checkout.checkout_status)

        # Check the item is referenced
        self.assertEqual(item, checkout.item)


class CheckoutManager_Checkout_TestCase(TestCase):
    fixtures = ["test_fixtures.json"***REMOVED***

    # Set a due date 4 days from now
    due_date = timezone.now() + timedelta(4)

    def test_good_checkout(self):
        ***REMOVED***
        Test that a perfect checkout entry passes through without a problem
        ***REMOVED***
        item = Item.objects.get(pk=1)

        manager.checkout_items(item, self.due_date)

        # Check the that the item availability is set correctly
        self.assertEqual(item.availability, "CHECKED_OUT")
        self.assertIsNone(Checkout.objects.get(pk=1).return_date)

    def test_good_checkout_multiple_items(self):
        ***REMOVED***
        Test that our checkout entry can have multiple items
        ***REMOVED***
        items = Item.objects.filter(availability="AVAILABLE")
        manager.checkout_items(items, self.due_date)

        # Iterator executes the query, so we're not looking into the cache.
        for item in items.iterator():
            self.assertEqual(item.availability, "CHECKED_OUT")

    def test_good_checkout_with_different_checkout_date(self):
        ***REMOVED***
        Check that we can set a checkout date in the ~future~
        ***REMOVED***
        items = Item.objects.filter(availability="AVAILABLE")
        checkout_date = self.due_date + timedelta(-2)
        manager.checkout_items(items, self.due_date, checkout_date=checkout_date)

        self.assertEqual(Checkout.objects.get(pk=1).checkout_date, checkout_date)

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


class CheckoutManager_Returns_TestCase(TestCase):

    # Fixtures are reinstalled after each test
    fixtures = ["test_fixtures.json"***REMOVED***

    def setUp(self):
        # Set up the checkout entry in the database
        self.items = Item.objects.filter(availability="AVAILABLE")

        # We checked this out 2 days ago
        self.checkout_date = timezone.now() + timedelta(-2)
        self.due_date = timezone.now() + timedelta(4)
        self.checkout = manager.checkout_items(
            self.items, self.due_date, checkout_date=self.checkout_date
        )[0***REMOVED***

    def test_good_return(self):
        manager.return_items(self.checkout)

        self.assertEqual(self.checkout.item.availability, "AVAILABLE")

        checkout = Checkout.objects.get(pk=1)
        self.assertIsNotNone(checkout.return_date)
        self.assertEqual(checkout.return_date.date(), timezone.now().date())

    def test_bad_return_date(self):
        ***REMOVED***
        Test that a return date must be after the checkout date
        ***REMOVED***
        item = self.checkout.item
        checkout_date = self.due_date
        # 60 days into the past
        return_date = timezone.now() + timedelta(-60)

        with self.assertRaises(ValidationError):
            manager.return_items(self.checkout, return_date=return_date)

        # Item should still be checked out
        self.assertEqual(item.availability, "CHECKED_OUT")


class CheckoutManager_Retrieve_TestCase(TestCase):

    fixtures = ["test_fixtures.json"***REMOVED***
    # ItemGroups with PK 1 and 3 are part of our test fixtures
    cart = {"1": 1, "3": 2***REMOVED***

    def test_good_retrieval(self):
        ***REMOVED***
        retrieve_items() should return a list of itmes that can be passed to checkout_items()
        ***REMOVED***
        # Expect retrieve_items() to return the first found items belonging to the ItemGroup
        expected = [
            Item.objects.filter(item_group_id=1).first(),
            Item.objects.get(pk=4),
            Item.objects.get(pk=5),
        ***REMOVED***

        result = manager.retrieve_items(self.cart)
        self.assertEqual(result, expected)

    def test_retrieval_only_returns_available_items(self):
        item = Item.objects.get(item_group_id=3, pk=4)
        item.availability = "UNAVAILABLE"
        item.save()

        expected = [
            Item.objects.filter(item_group_id=1).first(),
            Item.objects.get(item_group_id=3, pk=5),
            Item.objects.get(item_group_id=3, pk=6),
        ***REMOVED***

        result = manager.retrieve_items(self.cart)
        self.assertEqual(result, expected)
