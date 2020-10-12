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


class LibrarianAuthTests(BiblioTechBaseTest):
    """
    Library management endpoints should be accessible ONLY to users in librarian group.
    """

    @parameterized.expand(
        [
            ("deny-checkout", {"username": "member", "password": "password"}, 403),
            ("deny-checkout", {"username": "librarian", "password": "password"}, 200),
            ("add-item", {"username": "member", "password": "password"}, 403),
            ("add-item", {"username": "librarian", "password": "password"}, 200),
            ("master-inventory", {"username": "member", "password": "password"}, 403),
            (
                "master-inventory",
                {"username": "librarian", "password": "password"},
                200,
            ),
            ("update-item", {"username": "member", "password": "password"}, 403),
            ("update-item", {"username": "librarian", "password": "password"}, 200),
            ("delete-item", {"username": "member", "password": "password"}, 403),
            ("delete-item", {"username": "librarian", "password": "password"}, 200),
        ]
    )
    def test_view_inacessible_to_unauthorized_users(self, reverse_string, user, status):
        """
        Unauthorized requests to the return item view should return 403
        """
        endpoint = ""

        if reverse_string == "deny-checkout":
            endpoint = reverse("deny-checkout", args=(self.checkout.id,))
        elif reverse_string in ["update-item", "delete-item"]:
            endpoint = reverse(reverse_string, args=(Item.objects.first().id,))
        else:
            endpoint = reverse(reverse_string)

        self.client.login(username=user["username"], password=user["password"])

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status)

    def test_authorized_approve_endpoint(self):
        """
        Valid requests to /checkout/<int>/approve should approve the request and redirect to
        the control panel
        """
        self.client.login(username="librarian", password="password")
        response = self.client.post(
            reverse("approve-checkout", args=(self.checkout.id,))
        )

        # Assert redirect
        self.assertRedirects(response, reverse("librarian-control-panel"))

        # Assert relevant objects are updated
        self.checkout.refresh_from_db()
        self.assertEqual(self.checkout.approval_status, "APPROVED")

    def test_unauthorized_approve_endpoint(self):
        """
        Invalid requests to /checkout/<int>/approve should return 403 for an unauthorized user
        """
        self.client.login(username="member", password="password")
        response = self.client.post(
            reverse("approve-checkout", args=(self.checkout.id,))
        )

        self.assertEqual(response.status_code, 403)


class LibrarianDenyTests(BiblioTechBaseTest):
    def setUp(self):
        super(LibrarianDenyTests, self).setUp()
        self.deny_endpoint = reverse("deny-checkout", args=(self.checkout.id,))

    @parameterized.expand(
        [
            ("librarian", "password", 200),
            ("member", "password", 403),
        ]
    )
    def test_authorized_deny_post(self, username, password, expected_status):
        """
        Valid request should redirect to control panel
        Non-librarian users should have 403 returned.
        """
        self.client.login(username=username, password=password)

        # Mimick a post request with data
        response = self.client.post(
            self.deny_endpoint, {"reason": "reason"}, follow=True
        )
        self.assertEqual(response.status_code, expected_status)

        # If we get a redirect as our status code, assert that we're redirect to the control panel
        if expected_status == 302:
            self.assertRedirects(reverse("librarian-control-panel"))

    def test_authorized_deny_post_blank_reason(self):
        self.client.login(username="librarian", password="password")

        response = self.client.post(self.deny_endpoint, {"reason": ""}, follow=True)
        self.assertContains(response, "This field is required")


class LibrarianReturnTests(BiblioTechBaseTest):
    @parameterized.expand(
        [
            ({"username": "member", "password": "password"}, 403),
            ({"username": "librarian", "password": "password"}, 200),
        ]
    )
    def test_view_inacessible_to_unauthorized_users(self, user, status):
        """
        Unauthorized requests to the return item view should return 403
        """
        self.client.login(username=user["username"], password=user["password"])

        response = self.client.get(reverse("return-item"))
        self.assertEqual(response.status_code, status)

    def test_post_with_invalid_checkout_id_returns_404(self):
        self.client.login(username="librarian", password="password")

        response = self.client.post(
            reverse("return-item"),
            {
                "checkout_id": 400,
                "is_verified": "true",
                "return_condition": "GOOD",
                "inspection_notes": "Some notes",
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_successful_return_flow(self):
        self.client.login(username="librarian", password="password")

        response = self.client.post(
            reverse("return-item"),
            {
                "checkout_id": self.checkout.id,
                "return_condition": "GOOD",
                "is_verified": "true",
                "inspection_notes": "",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("librarian-control-panel"))

        # Validate related objects
        self.checkout.refresh_from_db()
        self.assertEqual(self.checkout.checkout_status, "RETURNED")
        self.assertEqual(self.checkout.item.availability, "AVAILABLE")

    def test_form_errors(self):
        self.client.login(username="librarian", password="password")

        response = self.client.post(
            reverse("return-item"),
            {
                "checkout_id": self.checkout.id,
                "return_condition": "",
                "is_verified": "",
                "inspection_notes": "",
            },
            follow=True,
        )

        self.assertTrue(response.context["form"].errors["is_verified"])
        self.assertTrue(response.context["form"].errors["return_condition"])
        self.assertIn(
            "management/return_item.html", [x.name for x in response.templates]
        )
        self.assertContains(
            response, "Please verify the item information matches the returning item"
        )
        self.assertContains(response, "This field is required")
