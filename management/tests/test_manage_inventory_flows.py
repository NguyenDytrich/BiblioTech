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


class DeleteItemFlowTests(BiblioTechBaseTest):
    def test_success_flow(self):
        self.client.login(username="librarian", password="password")
        expected_model = Item.objects.get(pk=1)
        url = reverse("delete-item", args=(expected_model.id,))
        response = self.client.post(
            url,
            {"item_id": 1, "item_name": str(expected_model), "is_sure": "TRUE"},
            follow=True,
        )

        self.assertRedirects(response, f"{reverse('master-inventory')}?active=1")

        with self.assertRaises(Item.DoesNotExist):
            Item.objects.get(pk=1)

    def test_item_id_mismatch(self):
        self.client.login(username="librarian", password="password")
        expected_model = Item.objects.get(pk=1)
        url = reverse("delete-item", args=(expected_model.id,))
        response = self.client.post(
            url,
            {"item_id": 1, "item_name": "notmatch", "is_sure": "TRUE"},
            follow=True,
        )
        self.assertContains(
            response, "This field must match the item identifier above!"
        )

    def test_empty_fields(self):
        self.client.login(username="librarian", password="password")
        expected_model = Item.objects.get(pk=1)
        url = reverse("delete-item", args=(expected_model.id,))
        response = self.client.post(
            url,
            {"item_id": "", "item_name": "", "is_sure": ""},
            follow=True,
        )
        self.assertContains(response, "This field is required.", count=2)


class UpdateItemFlowTests(BiblioTechBaseTest):
    def test_success_redirect(self):
        """
        Should return properly
        """
        self.client.login(username="librarian", password="password")
        expected_model = Item.objects.get(pk=1)
        url = reverse("update-item", args=(expected_model.id,))
        response = self.client.post(
            url,
            {"availability": "AVAILABLE", "condition": "GOOD", "notes": ""},
            follow=True,
        )

        self.assertRedirects(response, f"{reverse('master-inventory')}?active=1")
