from django.test import TestCase
from equilizer.models import Item, ItemGroup


class ItemModelTest(TestCase):
    ***REMOVED***
    Test how Item objects interact with ItemGroup objects
    ***REMOVED***

    def test_item_string_repr(self):
        ***REMOVED***
        Assert that if an item has no library id, it uses the parent's inmake, modle, and the item's serial number.
        ***REMOVED***
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
        self.assertEqual(str(item), f"{group.make***REMOVED*** {group.model***REMOVED*** sn. {item.serial_num***REMOVED***")

    def test_item_string_repr_moniker(self):
        ***REMOVED***
        Assert string representation uses a moniker over make/model
        ***REMOVED***
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

        self.assertEqual(str(item), f"{group.moniker***REMOVED*** sn. {item.serial_num***REMOVED***")

    def test_item_string_repr_lib_id(self):
        ***REMOVED***
        Assert library id takes priority over string representation
        ***REMOVED***
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

        self.assertEqual(str(item), f"{item.library_id***REMOVED***")
