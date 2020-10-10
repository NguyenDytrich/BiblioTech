from datetime import timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.test import TestCase

from library.models import Checkout, Item, Member
from library.tests.utils import BiblioTechBaseTest
import library.checkout_manager as manager


class CheckoutManager_Returns_TestCase(TestCase):
    """
    Test return-related checkout-manager functions
    """

    # Fixtures are reinstalled after each test
    fixtures = ["test_fixtures.json"]

    def setUp(self):
        # Set up a user in hte database
        self.user = User.objects.create(username="member", email="member@test.edu")
        self.user.set_password("password")
        self.user.save()

        member = Member.objects.create(user=self.user, organization_id=1, member_id="MEMBER1")
        member.save()

        # Set up the checkout entry in the database
        self.items = Item.objects.filter(availability="AVAILABLE")

        # We checked this out 2 days ago
        self.checkout_date = timezone.now() + timedelta(-2)
        self.due_date = timezone.now() + timedelta(4)
        self.checkout = manager.checkout_items(
            self.items, self.due_date, self.user, checkout_date=self.checkout_date
        )[0]

    def test_good_return(self):
        manager.return_items(self.checkout)

        self.assertEqual(self.checkout.item.availability, "AVAILABLE")

        checkout = Checkout.objects.get(pk=1)
        self.assertIsNotNone(checkout.return_date)
        self.assertEqual(checkout.return_date.date(), timezone.now().date())
        self.assertEqual(checkout.checkout_status, "RETURNED")

    def test_bad_return_date(self):
        """
        Test that a return date must be after the checkout date
        """
        item = self.checkout.item
        # 60 days into the past
        return_date = timezone.now() + timedelta(-60)

        with self.assertRaises(ValidationError):
            manager.return_items(self.checkout, return_date=return_date)

        # Item should still be checked out
        self.assertEqual(item.availability, "CHECKED_OUT")


class CheckoutManager_Approval_Tests(BiblioTechBaseTest):
    """
    Test approval behavior for checkout_manager
    """

    fixtures = ["test_fixtures.json"]

    def setUp(self):
        # Create a test user in the database
        self.user = User.objects.create(username="member", email="member@test.edu")
        self.user.set_password("password")
        self.user.save()

        member = Member.objects.create(user=self.user, organization_id=1, member_id="MEMBER1")
        member.save()

        # Set a due date 4 days from now
        self.due_date = timezone.now() + timedelta(4)

        # Create a checkout entry
        self.item_id = 1
        self.checkout = manager.checkout_items(
            Item.objects.get(pk=self.item_id), self.due_date, self.user
        )[
            0
        ]  # Checkout_items returns a list, so take the 1st item

    def test_approval(self):
        """
        Assert method should set approval status correctly
        """
        checkout = self.checkout
        manager.approve_checkout(checkout)
        database_obj = Checkout.objects.get(pk=checkout.id)
        self.assertEqual(database_obj.approval_status, "APPROVED")

    def test_deny(self):
        """
        Assert method updates related objects correctly
        """
        checkout = self.checkout
        item = checkout.item

        manager.deny_checkout(checkout)

        db_checkout = Checkout.objects.get(pk=checkout.id)
        db_item = Item.objects.get(pk=item.id)

        self.assertEqual(db_checkout.approval_status, "DENIED")
        self.assertEqual(db_checkout.checkout_status, "RETURNED")
        self.assertEqual(db_item.availability, "AVAILABLE")
