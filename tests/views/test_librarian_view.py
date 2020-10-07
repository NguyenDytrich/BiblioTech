from django.urls import reverse

from bibliotech.views.librarian import (
    LibrarianView,
    AddHoldingView,
    MasterInventoryView,
    UpdateItemView,
)
from bibliotech.models import Checkout, ItemGroup, Item

from tests.utils import BiblioTechBaseTest


class LibrarianViewTests(BiblioTechBaseTest):
    def setUp(self):
        super(LibrarianViewTests, self).setUp()
        self.deny_endpoint = reverse("deny-checkout", args=(self.checkout.id,))

    def test_authorized_deny_post_blank_reason(self):
        self.client.login(username="librarian", password="password")

        response = self.client.post(self.deny_endpoint, {"reason": ""}, follow=True)
        self.assertContains(response, "This field is required")

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


class AddHoldingViewTests(BiblioTechBaseTest):
    def setUp(self):
        self.view = AddHoldingView()

    def test_queryset(self):
        self.assertEqual(list(self.view.queryset), list(ItemGroup.objects.all()))


class MasterInventoryViewTests(BiblioTechBaseTest):
    def setUp(self):
        super(MasterInventoryViewTests, self).setUp()
        self.view = MasterInventoryView()

    def test_queryset(self):
        """
        View should have the specified information
        """
        self.assertEqual(list(self.view.queryset), list(ItemGroup.objects.all()))

    def test_context(self):
        """
        View should have an active_item_set variable when there is an active item group selected.
        """
        self.client.login(username="librarian", password="password")

        # In this test we are getting the Nikon D7000 itemgroup fixture
        response = self.client.get(f"{reverse('master-inventory')}?active=1")

        # There is exactly 1 D7000 item entry
        self.assertTrue(response.context.get("active_item_set"))
        self.assertEqual(1, response.context.get("active_item_set").count())

class UpdateItemViewTests(BiblioTechBaseTest):
    def setUp(self):
        super(UpdateItemViewTests, self).setUp()
        self.view = UpdateItemView()

    def test_context_data(self):
        """
        View should have the specified object in the context
        """
        self.client.login(username="librarian", password="password")

        expected_model = Item.objects.get(pk=1)
        url = reverse("update-item", args=(expected_model.id,))
        response = self.client.get(url)
        self.assertEqual(response.context.get("object"), expected_model)
