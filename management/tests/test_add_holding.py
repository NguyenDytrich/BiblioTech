from datetime import timedelta
from django.contrib.auth.models import User, Group
from django.test import TestCase, TransactionTestCase
from django.utils import timezone
from django.urls import reverse
from parameterized import parameterized
import unittest

import library.checkout_manager as checkout_manager
from library.models import Checkout, Item, ItemGroup

from library.tests.utils import BiblioTechBaseTest


class AddHoldingTests(BiblioTechBaseTest):
    def test_add_item(self):
        self.client.login(username="librarian", password="password")

        response = self.client.post(
            reverse("add-item"),
            {
                "make": "Shure",
                "model": "SM57",
                "description": "Good microphone",
                "moniker": "SM57",
                "default_checkout_len": 7,
            },
            follow=True,
        )

        self.assertContains(response, "successfully added to catalogue")
        self.assertTrue(ItemGroup.objects.filter(moniker="SM57").exists())

    def test_add_item_missing_fields(self):
        self.client.login(username="librarian", password="password")

        response = self.client.post(
            reverse("add-item"),
            {
                "make": "",
                "model": "",
                "description": "",
                "moniker": "",
            },
            follow=True,
        )

        self.assertIn("management/add_item.html", [x.name for x in response.templates])
        self.assertContains(response, "This field is required", count=4)

    def test_add_item_sanitized_description(self):
        self.client.login(username="librarian", password="password")
        fields = {
            "make": "Shure",
            "model": "SM57",
            "description": "a test <script>What if this</script><p onClick='nobueno_func()'>This?</p><p>How about some valid stuff</p>",
            "moniker": "SM57",
            "default_checkout_len": 7,
        }

        response = self.client.post(reverse("add-item"), fields, follow=True)
        self.assertEqual(response.status_code, 200)
        item = ItemGroup.objects.filter(moniker="SM57").first()

        # They should not be equal, as the input should be sanitized.
        self.assertNotEqual(fields["description"], item.description)
        self.assertEqual(
            "<div>a test <p>This?</p><p>How about some valid stuff</p></div>",
            item.description,
        )

    # TODO: might have to swap names of item vs holding?
    def test_add_holding(self):
        self.client.login(username="librarian", password="password")

        response = self.client.post(
            reverse("add-holding"),
            {
                "is_verified": "TRUE",
                "itemgroup_id": "1",
                "library_id": "Nikon-D7000-2",
                "serial_num": "0002",
                "availability": "AVAILABLE",
                "condition": "EXCELLENT",
                "notes": "Some notes",
            },
            follow=True,
        )

        self.assertContains(response, "successfully added to inventory.")
        self.assertTrue(Item.objects.filter(library_id="Nikon-D7000-2").exists())

    def test_add_holding_missing_fields(self):
        self.client.login(username="librarian", password="password")

        response = self.client.post(
            reverse("add-holding"),
            {
                "is_verified": "",
                "library_id": "",
                "serial_num": "",
                "availability": "",
                "condition": "",
                "notes": "",
            },
        )

        self.assertIn(
            "management/add_holding.html", [x.name for x in response.templates]
        )
        self.assertContains(
            response,
            "Please verify the item information matches the new holding",
            count=1,
        )
        self.assertContains(response, "This field is required", count=4)

    def test_add_holding_unique_violation(self):
        self.client.login(username="librarian", password="password")

        item = self.item

        response = self.client.post(
            reverse("add-holding"),
            {
                "is_verified": "TRUE",
                "itemgroup_id": item.item_group_id,
                "library_id": item.library_id,
                "serial_num": item.serial_num,
                "availability": "AVAILABLE",
                "condition": "GOOD",
                "notes": "",
            },
            follow=True,
        )

        self.assertContains(
            response, f"Library id {item.library_id} already in system!"
        )
        self.assertContains(
            response, f"Serial number {item.serial_num} already in system!"
        )
