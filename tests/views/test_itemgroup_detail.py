from django.test import TestCase
from django.urls import reverse

from equilizer.models import ItemGroup


class ItemGroupDetailTests(TestCase):
    fixtures = ["test_fixtures.json"***REMOVED***

    itemgroup = ItemGroup.objects.get(pk=1)
    url = reverse("itemgroup-detail", args=(itemgroup.id,))

    def test_detail_shows_make(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.itemgroup.make)

    def test_detail_shows_model(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.itemgroup.model)

    def test_detail_shows_desc(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.itemgroup.description)
