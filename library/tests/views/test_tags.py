from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from library.models import ItemGroup, Tag


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
        # self.item_group.tags.add(self.tag)

        # Save the models
        self.item_group.save()
        self.tag.save()

    def test_add_tag(self):
        """
        POST requests to .../items/<pk>/tags should add a tag
        """

        self.client.post(
            reverse("itemgroup-taglist", args=(self.item_group.id,)),
            {"tag_name": "test"},
        )
        self.assertIn(self.tag, list(self.item_group.tags.all()))
