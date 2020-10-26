from django.test import TestCase
from library.models import ItemGroup, Tag
from parameterized import parameterized


class ItemGroupTagTests(TestCase):
    def setUp(self):
        # Create an item group
        self.item_group = ItemGroup.objects.create(
            make="Make",
            model="model",
            description="description",
            default_checkout_len=7,
        )

        # Create a tag
        self.tag = Tag.objects.create(name="Test")

        # Add tag to itemgroup
        self.item_group.tags.add(self.tag)

        # Save the models
        self.item_group.save()
        self.tag.save()
