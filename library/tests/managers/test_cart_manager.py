from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized

import library.cart_manager as manager
from library.models import ItemGroup
from library.validators import CartValidator as validator


class CartManagerTests(TestCase):
    """
    Tests for the cart_manager
    """

    fixtures = ["test_fixtures.json"]

    def setUp(self):
        self.cart = dict()

    def test_good_add_to_cart(self):
        """
        Assert that add_to_cart() mutates the passed dictionary as expected
        """
        item = ItemGroup.objects.get(pk=1)
        str_id = str(item.id)

        manager.add_to_cart(self.cart, item.id)

        self.assertIn(str_id, self.cart)
        self.assertEqual(self.cart[str_id], 1)

    def test_good_add_to_cart_multiple(self):
        item = ItemGroup.objects.get(pk=1)
        num = item.avail_inventory()
        str_id = str(item.id)

        for i in range(num):
            manager.add_to_cart(self.cart, item.id)

        self.assertIn(str_id, self.cart)
        self.assertEqual(self.cart[str_id], num)

    def test_erroneous_input(self):
        """
        Assert that add_to_cart() expects a Dict as its first argument
        """
        with self.assertRaisesMessage(
            TypeError, "Expected `cart` to be Dict but found <class 'str'>"
        ):
            manager.add_to_cart("", 1)

    def test_retrieval(self):
        """
        Assert that the cart manager can retrieve displayable data
        """
        item = ItemGroup.objects.get(pk=3)
        str_id = str(item.id)
        cart = {str_id: 2}

        dto = manager.retrieve_for_display(cart)

        for d in dto:
            self.assertEqual(
                {key: d[key] for key in ["name", "quantity"]},
                {"name": str(item), "quantity": cart[str_id]},
            )
            self.assertTrue(d.get("return_date"))

    @parameterized.expand(["UNAVAILABLE", "CHECKED_OUT", "HOLD", "LOST"])
    def test_bad_add_to_cart_no_inventory(self, avail):
        """
        Assert that add_to_cart() returns an error if there is no inventory for
        a requested item, and does not mutate the dictionary
        """
        itemgroup = ItemGroup.objects.get(pk=1)
        item = itemgroup.item_set.first()

        # Set all items in the set to an unavailbility condition
        item.availability = avail
        item.save()

        with self.assertRaises(ValidationError):
            manager.add_to_cart(self.cart, item.id)

        # Our cart was empty, so it shouldn't create a key-value pair
        self.assertNotIn(item.id, self.cart)

    def test_bad_add_to_cart_would_exceed_inventory(self):
        """
        If adding to cart would excede the avail_inventory, it should raise
        an exception.
        """
        item = ItemGroup.objects.get(pk=1)

        # Simulate adding all available items into the cart
        for i in range(item.avail_inventory()):
            manager.add_to_cart(self.cart, item.id)

        with self.assertRaises(ValidationError):
            manager.add_to_cart(self.cart, item.id)


class CartValidatorTests(TestCase):
    """
    Tests for the CartValidator
    """

    fixtures = ["test_fixtures.json"]

    def test_has_inventory(self):
        """
        Assert that if an item group has available inventory, it passes validation
        """
        itemgroup = ItemGroup.objects.get(pk=1)
        try:
            validator.has_inventory(itemgroup)
        except ValidationError:
            self.fail()

    # Expand the test to take all of our unavailability conditions
    @parameterized.expand(["UNAVAILABLE", "CHECKED_OUT", "HOLD", "LOST"])
    def test_not_has_inventory(self, avail):
        """
        Assert that if an item has no available inventory (avail_inventory is 0),
        it fails validation
        """
        itemgroup = ItemGroup.objects.get(pk=1)
        items = itemgroup.item_set.all()
        # Set all items in the set to an unavailbility condition
        for i in items:
            i.availability = avail
            i.save()

        with self.assertRaises(ValidationError):
            validator.has_inventory(itemgroup)

    def test_does_not_exceed_avail_inventory(self):
        """
        Nothing should happen if adding an item to the cart will not exceed the
        available inventory
        """
        # Set up some test data
        cart = dict()
        item = ItemGroup.objects.get(pk=1)

        try:
            validator.does_not_exceed(cart, item)
        except ValidationError:
            self.fail()

    def test_would_exceeed_avail_inventory(self):
        """
        If adding an item to the cart will exceed the available inventory, raise
        exception.
        """
        # Set up some test data
        cart = dict()
        item = ItemGroup.objects.get(pk=1)
        avail = item.avail_inventory()
        str_id = str(item.id)

        cart[str_id] = avail

        with self.assertRaises(ValidationError):
            validator.does_not_exceed(cart, item)
