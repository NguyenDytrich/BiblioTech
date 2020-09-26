from django.test import TestCase

import equilizer.cart_manager as manager
from equilizer.models import Item, ItemGroup


class CartManagerTests(TestCase):
    fixtures = ["test_fixtures.json"***REMOVED***

    def test_good_add_to_cart(self):
        cart = dict()
        item = ItemGroup.objects.get(pk=1)
        item_id = str(item.id)

        manager.add_to_cart(cart, item_id)

        self.assertIn(item_id, cart)
        self.assertEqual(cart[item_id***REMOVED***, 1)

    def test_erroneous_input(self):
        with self.assertRaisesMessage(
            TypeError, "Expected `cart` to be Dict but found <class 'str'>"
        ):
            manager.add_to_cart("", 1)
