from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from unittest import mock

from library.models import Checkout, Item


class CheckoutClassTestCase(TestCase):
    """
    Test the class behaviors NOT the object behaviors.
    """

    def test_checkout_string_repr(self):
        """
        Assert that checkout string representation is human-readable
        """
        item = Item(library_id="Test")
        date = datetime.now()
        checkout = Checkout(item=item, checkout_date=date)
        self.assertEqual(str(checkout), "Test")

    def test_checkout_enum_choices(self):
        """
        Assert that the specified values exist in the enumerable classes
        """
        enum_approval_status = ["APPROVED", "DENIED", "PENDING"]
        enum_checkout_status = ["RETURNED", "OVERDUE", "LOST", "OUTSTANDING"]

        for approval_status in enum_approval_status:
            self.assertEqual(Checkout.ApprovalStatus[approval_status], approval_status)

        for checkout_status in enum_checkout_status:
            self.assertEqual(Checkout.CheckoutStatus[checkout_status], checkout_status)

    def test_checkout_returned_defaults_null(self):
        """
        Assert that new Checkout instances default Checkout.return_date to null
        """
        checkout = Checkout()
        self.assertIsNone(checkout.return_date)

    def test_checkout_returned_accepts_null(self):
        """
        Assert that new Checkout instances can take None in their constructor
        """
        checkout = Checkout(return_date=None)
        self.assertIsNone(checkout.return_date)

    def test_checkout_status_defaults_outstanding(self):
        """
        Assert that new Checkout instances default Checkout.checkout_status to OUTSTANDING
        """
        checkout = Checkout()
        self.assertEqual(
            Checkout.CheckoutStatus["OUTSTANDING"], checkout.checkout_status
        )

    def test_checkout_approval_default_pending(self):
        """
        Assert that new Checkout instances default Checkout.approval_status to PENDING
        """
        checkout = Checkout()
        self.assertEqual(Checkout.ApprovalStatus["PENDING"], checkout.approval_status)

    @freeze_time("2000-01-01")
    def test_checkout_date_defaults_now(self):
        """
        Assert that Checkout.checkout_date defaults to datetime.now
        """

        # Mock the default checkout_date field to be a function operating within
        # the freezegun scope

        field = Checkout._meta.get_field("checkout_date")
        with mock.patch.object(field, "default", new=timezone.now()):
            checkout = Checkout()
            self.assertEqual(checkout.checkout_date, timezone.now())


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
