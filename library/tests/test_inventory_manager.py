from datetime import datetime, timedelta
from django.utils import timezone
from django.test import TestCase

from library.models import Item, ItemGroup
import management.inventory_manager as manager


class InventoryManagerTests(TestCase):
    fixtures = ["test_fixtures.json"]

    def test_good_create_item_record(self):
        # Omit optional fields
        item = manager.create_item_record(1, "Test-1", "TEST000", "GOOD", "UNAVAILABLE")

        past_acquired = timezone.now() + timedelta(-5)
        past_inspected = timezone.now() + timedelta(-4)

        # Item with optional fields
        item2 = manager.create_item_record(
            1,
            "Test-2",
            "TEST001",
            "GOOD",
            "UNAVAILABLE",
            notes="Some notes",
            date_acquired=past_acquired,
            last_inspected=past_inspected,
        )

        # the manager will return the item record if no errors occur
        self.assertTrue(item)
        self.assertTrue(item2)

        # Verify that fields are set correctly
        self.assertEqual("Some notes", item2.notes)

    def test_good_create_itemgroup_record(self):
        # Omit optional fields
        itemgroup = manager.create_itemgroup_record("Test", "Model", "A test object")

        # With optional fields
        itemgroup2 = manager.create_itemgroup_record(
            "Test", "Model", "A test object", "Test Model Moniker"
        )

        # Manager returns items if no errors occur
        self.assertTrue(itemgroup)
        self.assertTrue(itemgroup2)

        # Verify optional fields are set correctly
        self.assertEqual("Test Model Moniker", itemgroup2.moniker)
