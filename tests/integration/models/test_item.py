from django.test import TestCase
from equilizer.models import Item, ItemGroup


class ItemIntegrationTestCase(TestCase):
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
