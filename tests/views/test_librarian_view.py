from django.urls import reverse

from bibliotech.views.librarian import LibrarianView, AddHoldingView
from bibliotech.models import Checkout, ItemGroup

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
