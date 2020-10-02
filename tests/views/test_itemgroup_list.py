from django.test import TransactionTestCase
from django.urls import reverse

from bibliotech.models import ItemGroup


class ItemGroupListTests(TransactionTestCase):
    fixtures = ["test_fixtures.json"***REMOVED***
    url = reverse("itemgroup-list")

    def test_make_model_rendered(self):
        response = self.client.get(self.url)
        for i in ItemGroup.objects.all():
            if i.moniker:
                self.assertContains(response, i.moniker)
            else:
                self.assertContains(response, f"{i.make***REMOVED*** {i.model***REMOVED***")
