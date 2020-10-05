from datetime import timedelta
from django.contrib.auth.models import User, Group
from django.test import TestCase, TransactionTestCase
from django.utils import timezone
from django.urls import reverse
from parameterized import parameterized

import bibliotech.checkout_manager as checkout_manager
from bibliotech.models import Checkout, Item
from bibliotech.class_views.admin_views import LibrarianView


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

        self.item_id = 5
        self.item = Item.objects.get(pk=self.item_id)

        # Select the first item since checkout manager returns a list
        self.checkout = checkout_manager.checkout_items(
            self.item,
            due_date,
            self.user,
        ).pop()


class LibrarianViewDataRetrieval(BiblioTechBaseTest):
    def test_get_pending_checkouts(self):
        """
        Assert that only pending checkouts are returned, and that they are sorted by
        date asc.
        """
        view = LibrarianView()
        expected = Checkout.objects.filter(approval_status="PENDING").order_by(
            "checkout_date"
        )

        dto = view.get_pending_checkouts()

        self.assertEqual(list(dto), list(expected))
        # Checkout date of the first item should be before the next item
        self.assertLess(list(dto)[0].checkout_date, list(dto)[1].checkout_date)


class LibrarianViewAuthTests(BiblioTechBaseTest):
    """
    Library management endpoints should be accessible ONLY to users in librarian group.
    """

    def setUp(self):
        super(LibrarianViewAuthTests, self).setUp()
        self.deny_endpoint = reverse("deny-checkout", args=(self.checkout.id,))

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

    @parameterized.expand(
        [
            ("librarian", "password", 200),
            ("member", "password", 403),
        ]
    )
    def test_authorized_deny_view(self, username, password, expected_status):
        """
        Valid get request to /checkout/<int>/deny should return a view
        Invalid get request should return 403
        """
        self.client.login(username=username, password=password)
        response = self.client.get(self.deny_endpoint)
        self.assertEqual(response.status_code, expected_status)

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


class LibrarianReturnViewTests(BiblioTechBaseTest):

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
                "return_condition": "GOOD",
                "inspection_notes": "Some notes",
            },
        )
        self.assertEqual(response.status_code, 404)
