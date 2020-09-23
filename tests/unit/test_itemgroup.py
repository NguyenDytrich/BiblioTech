from django.test import TestCase
from equilizer.models import ItemGroup


class ItmeGroupUnitTestCase(TestCase):
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
