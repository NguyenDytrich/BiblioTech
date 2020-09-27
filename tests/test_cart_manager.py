from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized

import equilizer.cart_manager as manager
from equilizer.models import Item, ItemGroup
from equilizer.validators import CartValidator


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


class CartValidatorTests(TestCase):
    fixtures = ["test_fixtures.json"***REMOVED***
    validator = CartValidator()

    def test_has_inventory(self):
        ***REMOVED***
        Assert that if an item group has available inventory, it passes validation
        ***REMOVED***
        itemgroup = ItemGroup.objects.get(pk=1)
        try:
            self.validator.has_inventory(itemgroup)
        except ValidationError:
            self.fail()

    # Expand the test to take all of our unavailability conditions
    @parameterized.expand(["UNAVAILABLE", "CHECKED_OUT", "HOLD", "LOST"***REMOVED***)
    def test_not_has_inventory(self, avail):
        ***REMOVED***
        Assert that if an item has no available inventory (avail_inventory is 0),
        it fails validation
        ***REMOVED***
        itemgroup = ItemGroup.objects.get(pk=1)
        items = itemgroup.item_set.all()
        # Set all items in the set to an unavailbility condition
        for i in items:
            i.availability = avail
            i.save()

        with self.assertRaises(ValidationError):
            self.validator.has_inventory(itemgroup)
