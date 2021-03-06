from django.urls import reverse

from management.views.librarian import (
    LibrarianView,
    AddHoldingView,
    MasterInventoryView,
    UpdateItemView,
)
from library.models import Checkout, ItemGroup, Item

from library.tests.utils import BiblioTechBaseTest


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
        self.client.login(username="librarian", password="password")

    def test_queryset(self):
        """
        View should have the specified information
        """
        self.assertEqual(list(self.view.queryset), list(ItemGroup.objects.all()))

    def test_context(self):
        """
        View should have an active_item_set variable when there is an active item group selected.
        """
        # In this test we are getting the Nikon D7000 itemgroup fixture
        response = self.client.get(f"{reverse('master-inventory')}?active=1")

        # There is exactly 1 D7000 item entry
        self.assertEqual(1, response.context.get("active").item_set.all().count())

    def test_about_view_query(self):
        """
        View should set an about_view parameter in the context.
        """
        response = self.client.get(f"{reverse('master-inventory')}?active=1&about_view=features")
        self.assertEqual(response.context.get("about_view"), "features")

    def test_about_view_invalid(self):
        """
        View should not set the about_view parameter unless we corresponding content
        """
        response = self.client.get(f"{reverse('master-inventory')}?active=1&about_view=notvalid")
        self.assertFalse(response.context.get("about_view"))


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

class DeleteItemViewTests(BiblioTechBaseTest):

    def test_context_data(self):
        self.client.login(username="librarian", password="password")

        expected_model = Item.objects.get(pk=1)
        url = reverse("delete-item", args=(expected_model.id,))
        response = self.client.get(url)
        self.assertEqual(response.context.get("object"), expected_model)
