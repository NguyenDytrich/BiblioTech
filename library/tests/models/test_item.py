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
            make="Nikon", model="D7000", description="Mid-range DSLR camera"
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

