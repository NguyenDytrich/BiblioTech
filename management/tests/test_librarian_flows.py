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
            ("update-itemgroup", {"username": "member", "password": "password"}, 403),
            ("update-itemgroup", {"username": "librarian", "password": "password"}, 200),
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
        elif reverse_string in ["update-itemgroup"]:
            endpoint = reverse(reverse_string, args=(ItemGroup.objects.first().id,))
        else:
            endpoint = reverse(reverse_string)

        self.client.login(username=user["username"], password=user["password"])

        get_response = self.client.get(endpoint)
        post_response = self.client.post(endpoint)
        if get_response:
            self.assertEqual(get_response.status_code, status)
        if post_response:
            self.assertEqual(get_response.status_code, status)

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


class LibrarianManageItemTests(BiblioTechBaseTest):
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
        self.assertEqual("<div>a test <p>This?</p><p>How about some valid stuff</p></div>", item.description)


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
