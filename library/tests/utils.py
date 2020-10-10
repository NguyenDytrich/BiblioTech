from datetime import timedelta
from django.contrib.auth.models import User, Group
from django.test import TestCase, TransactionTestCase
from django.utils import timezone

import library.checkout_manager as checkout_manager
from library.models import Checkout, Item


class BiblioTechBaseTest(TransactionTestCase):

    fixtures = ["test_fixtures.json"]

    def setUp(self):
        # Create the librarian group
        librarian_group = Group.objects.get_or_create(name="librarian")[0]

        # Create two test users
        self.user = User.objects.create(username="member", email="member@test.edu")
        self.user.set_password("password")
        self.user.save()

        self.user2 = User.objects.create(username="member_2", email="member@test.edu")
        self.user2.set_password("password")
        self.user2.save()

        # Librarian user
        self.librarian = User.objects.create(
            username="librarian", email="librarian@test.edu"
        )
        self.librarian.set_password("password")
        self.librarian.groups.add(librarian_group)
        self.librarian.save()

        # Create some checkouts
        due_date = timezone.now() + timedelta(5)
        past_checkout_date = timezone.now() + timedelta(-5)
        self.items = [Item.objects.get(pk=1), Item.objects.get(pk=2)]

        # Checkout 2 items on different dates
        checkout_manager.checkout_items(self.items[0], due_date, self.user)
        checkout_manager.checkout_items(
            self.items[1], due_date, self.user, checkout_date=past_checkout_date
        )

        # Checkout, then return an item
        c = checkout_manager.checkout_items(
            Item.objects.get(pk=4), due_date, self.user
        ).pop()
        c.approval_status = "APPROVED"
        c.save()
        checkout_manager.return_items(c)

        # Variables for tests that need an item and corresponding checkout
        self.item_id = 5
        self.item = Item.objects.get(pk=self.item_id)

        # Select the first item since checkout manager returns a list
        self.checkout = checkout_manager.checkout_items(
            self.item,
            due_date,
            self.user,
        ).pop()
