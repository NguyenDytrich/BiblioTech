from django.test import TestCase
from django.db.models import ProtectedError
from equilizer.models import ItemGroup, Item


class ItemGroupTestCase(TestCase):
    def test_itemgroup_string_repr(self):
        ***REMOVED***
        Assert that item group string representation is human-readable
        ***REMOVED***
        make = "Nikon"
        model = "D7000"
        itmg = ItemGroup(make=make, model=model)
        self.assertEqual(str(itmg), f"{make***REMOVED*** {model***REMOVED***")

    def test_itemgroup_moniker_repr(self):
        ***REMOVED***
        Assert that if an item has a moniker, that is returned instead of the
        make/model
        ***REMOVED***
        moniker = "The D7000"
        itmg = ItemGroup(moniker=moniker)
        self.assertEqual(str(itmg), moniker)

    def test_delete_item_group_with_children(self):
        ***REMOVED***
        Assert that trying to delete item groups that have children throws an error
        ***REMOVED***
        group = ItemGroup.objects.create(
            make="Nikon", model="D7000", description="Mid range DSLR camera"
        )
        group.save()

        item = Item.objects.create(
            item_group=group, serial_num="0000", library_id="D7000-1"
        )
        item.save()

        with self.assertRaises(ProtectedError):
            group.delete()
