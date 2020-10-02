from django.test import TestCase
from django.db.models import ProtectedError
from bibliotech.models import ItemGroup, Item
from parameterized import parameterized


class ItemGroupClassTests(TestCase):
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


class ItemGroupTests(TestCase):
    ***REMOVED***
    ItemGroups with IDs 1 and 2 are defined within test_fixtures, hence the
    parameterized.expand with magic numbers.
    ***REMOVED***

    fixtures = ["test_fixtures.json"***REMOVED***

    @parameterized.expand([(1,), (2,)***REMOVED***)
    def test_total_inventory(self, pk):
        ***REMOVED***
        Assert that ItemGroup.total_inventory() returns the sum of all Items
        belonging to that ItemGroup
        ***REMOVED***
        itemg = ItemGroup.objects.get(pk=pk)
        total_items = itemg.item_set.all()

        self.assertEqual(itemg.total_inventory(), len(total_items))

    @parameterized.expand([(1,), (2,)***REMOVED***)
    def test_avail_items(self, pk):
        ***REMOVED***
        Assert that ItemGroup.avail_items() returns a set of available Items
        belonging to that ItemGroup
        ***REMOVED***
        itemg = ItemGroup.objects.get(pk=pk)
        avail_items = itemg.avail_items()
        actual_avail = Item.objects.filter(item_group=itemg, availability="AVAILABLE")

        self.assertSetEqual(avail_items, actual_avail)

    @parameterized.expand([(1,), (2,)***REMOVED***)
    def test_avail_inventory(self, pk):
        ***REMOVED***
        Assert that ItemGroup.avail_inventory() returns the sum of available items
        ***REMOVED***
        itemg = ItemGroup.objects.get(pk=pk)
        actual_avail = Item.objects.filter(item_group=itemg, availability="AVAILABLE")

        self.assertEqual(itemg.avail_inventory(), len(actual_avail))
