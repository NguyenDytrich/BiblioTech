from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from bibliotech.models import Checkout, Item


class CheckoutTestCase(TestCase):
    fixtures = ["test_fixtures.json"]
    due_date = timezone.now() + timedelta(4)

    def setUp(self):
        # Create a test user in the database
        self.user = User.objects.create(username="member", email="member@test.edu")
        self.user.set_password("password")
        self.user.save()

    def test_good_checkout(self):
        """
        Test a perfectly good checkout entry.
        """
        item = Item.objects.get(pk=1)
        checkout = Checkout.objects.create(
            due_date=self.due_date, item=item, user=self.user
        )

        checkout.save()

        # Check default values
        self.assertEqual("PENDING", checkout.approval_status)
        self.assertEqual("OUTSTANDING", checkout.checkout_status)

        # Check the item is referenced
        self.assertEqual(item, checkout.item)
