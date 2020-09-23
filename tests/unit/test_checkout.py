from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from equilizer.models import Checkout
from freezegun import freeze_time
from unittest import mock


class CheckoutUnitTestCase(TestCase):
    def test_checkout_string_repr(self):
        ***REMOVED***
        Assert that checkout string representation is human-readable
        ***REMOVED***

        date = datetime.now()
        checkout = Checkout(checkout_date=date)
        self.assertEqual(str(checkout), f"{date***REMOVED***")

    def test_checkout_enum_choices(self):
        ***REMOVED***
        Assert that the specified values exist in the enumerable classes
        ***REMOVED***
        enum_approval_status = ["APPROVED", "DENIED", "PENDING"***REMOVED***
        enum_checkout_status = ["RETURNED", "OVERDUE", "LOST", "OUTSTANDING"***REMOVED***

        for approval_status in enum_approval_status:
            self.assertEqual(Checkout.ApprovalStatus[approval_status***REMOVED***, approval_status)

        for checkout_status in enum_checkout_status:
            self.assertEqual(Checkout.CheckoutStatus[checkout_status***REMOVED***, checkout_status)

    def test_checkout_returned_defaults_null(self):
        ***REMOVED***
        Assert that new Checkout instances default Checkout.return_date to null
        ***REMOVED***
        checkout = Checkout()
        self.assertIsNone(checkout.return_date)

    def test_checkout_returned_accepts_null(self):
        ***REMOVED***
        Assert that new Checkout instances can take None in their constructor
        ***REMOVED***
        checkout = Checkout(return_date=None)
        self.assertIsNone(checkout.return_date)

    def test_checkout_status_defaults_outstanding(self):
        ***REMOVED***
        Assert that new Checkout instances default Checkout.checkout_status to OUTSTANDING
        ***REMOVED***
        checkout = Checkout()
        self.assertEqual(
            Checkout.CheckoutStatus["OUTSTANDING"***REMOVED***, checkout.checkout_status
        )

    def test_checkout_approval_default_pending(self):
        ***REMOVED***
        Assert that new Checkout instances default Checkout.approval_status to PENDING
        ***REMOVED***
        checkout = Checkout()
        self.assertEqual(Checkout.ApprovalStatus["PENDING"***REMOVED***, checkout.approval_status)

    @freeze_time("2000-01-01")
    def test_checkout_date_defaults_now(self):
        ***REMOVED***
        Assert that Checkout.checkout_date defaults to datetime.now
        ***REMOVED***

        # Mock the default checkout_date field to be a function operating within
        # the freezegun scope

        field = Checkout._meta.get_field("checkout_date")
        with mock.patch.object(field, "default", new=timezone.now()):
            checkout = Checkout()
            self.assertEqual(checkout.checkout_date, timezone.now())
