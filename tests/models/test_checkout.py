from datetime import datetime
from datetime import timedelta
from django.test import TestCase
from equilizer.models import Checkout, Item


class CheckoutTestCase(TestCase):
    fixtures = ["test_fixtures.json"***REMOVED***

    def test_good_checkout(self):
        ***REMOVED***
        Test a perfectly good checkout entry.
        ***REMOVED***
        item = Item.objects.get(pk=1)
        checkout = Checkout.objects.create(due_date=datetime.now() + timedelta(4))

        checkout.items.add(item)
        checkout.save()

        # Check default values
        self.assertEqual("PENDING", checkout.approval_status)
        self.assertEqual("OUTSTANDING", checkout.checkout_status)

        # Check the item is referenced
        self.assertEqual(item, checkout.items.all()[0***REMOVED***)
