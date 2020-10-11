from django.db import IntegrityError
from django.test import TestCase
from library.models import Item, ItemGroup


class ItemModelTest(TestCase):
    """
    Test how Item objects interact with ItemGroup objects
    """

    def test_item_string_repr(self):
        """
        Assert that if an item has no library id, it uses the parent's inmake, modle, and the item's serial number.
        """
        group = ItemGroup.objects.create(
            make="Nikon",
            model="D7000",
            description="Mid-range DSLR camera",
            default_checkout_len=7,
        )

        group.save()

        item = Item.objects.create(
            item_group=group,
            library_id="",
            serial_num="0000",
        )

        item.save()
        self.assertEqual(str(item), f"{group.make} {group.model} sn. {item.serial_num}")

    def test_item_string_repr_moniker(self):
        """
        Assert string representation uses a moniker over make/model
        """
        group = ItemGroup.objects.create(
            make="Nikon",
            model="D7000",
            moniker="Nikon-D7000",
            description="Mid-range DSLR camera",
            default_checkout_len=7,
        )

        group.save()

        item = Item.objects.create(
            item_group=group,
            library_id="",
            serial_num="0000",
        )
        item.save()

        self.assertEqual(str(item), f"{group.moniker} sn. {item.serial_num}")

    def test_item_string_repr_lib_id(self):
        """
        Assert library id takes priority over string representation
        """
        group = ItemGroup.objects.create(
            make="Nikon",
            model="D7000",
            moniker="Nikon-D7000",
            description="Mid-range DSLR camera",
            default_checkout_len=7,
        )
        group.save()

        item = Item.objects.create(
            item_group=group,
            library_id="Library-Id-1",
            serial_num="0000",
        )
        item.save()

        self.assertEqual(str(item), f"{item.library_id}")

    def test_item_unique_lib_id(self):
        """
        Assert that library ids are unique
        """
        group = ItemGroup.objects.create(
            make="Nikon",
            model="D7000",
            moniker="Nikon-D7000",
            description="Mid-range DSLR camera",
            default_checkout_len=7,
        )
        group.save()

        item = Item.objects.create(
            item_group=group,
            library_id="Library-Id-1",
            serial_num="0000",
        )
        item.save()

        with self.assertRaises(IntegrityError):
            item2 = Item.objects.create(
                item_group=group,
                library_id="Library-Id-1",
                serial_num="0001",
            )
            item2.save()


class ItemCompositeUniqueness(TestCase):
    def setUp(self):
        self.group = ItemGroup.objects.create(
            make="Nikon",
            model="D7000",
            moniker="Nikon-D7000",
            description="Mid-range DSLR camera",
            default_checkout_len=7,
        )
        self.group.save()

        self.group2 = ItemGroup.objects.create(
            make="Canon",
            model="5D",
            moniker="Canon-D5",
            description="Professional grade DSLR camera",
            default_checkout_len=7,
        )
        self.group2.save()

    def test_itemitemgroup_unique_violation(self):
        """
        (serial_num, ItemGroup) should be unique
        """
        with self.assertRaises(IntegrityError):
            item = Item.objects.create(
                item_group=self.group,
                library_id="Library-Id-1",
                serial_num="0000",
            )
            item.save()

            item = Item.objects.create(
                item_group=self.group,
                library_id="Library-Id-2",
                serial_num="0000",
            )
            item.save()

    def test_itemgroup_unique(self):
        """
        Should not throw any errors if there is a duplicate serial number so long
        as it belongs to a separate ItemGroup
        """

        item = Item.objects.create(
            item_group=self.group,
            library_id="Library-Id-2",
            serial_num="0000",
        )
        item.save()
        self.assertTrue(item)

        item = Item.objects.create(
            item_group=self.group2,
            library_id="Library-id-1",
            serial_num="0000",
        )
        item.save()
        self.assertTrue(item)
