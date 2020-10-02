from django.test import TransactionTestCase
from django.urls import reverse

from bibliotech.models import ItemGroup

class CartViewTests(TransactionTestCase):
    fixtures = ["test_fixtures.json"***REMOVED***

    def test_view_renders_items(self):
        item = ItemGroup.objects.get(pk=3)
        count = 2
        str_id = str(item.id)
        cart = {str_id: count***REMOVED***

        session = self.client.session
        session["cart"***REMOVED*** = cart
        session.save()

        response = self.client.get(reverse("cart-view"))

        self.assertContains(response, str(item))
        self.assertContains(response, f"x{count***REMOVED***")
