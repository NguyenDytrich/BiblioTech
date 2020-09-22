from django.test import TestCase
from equilizer.models import Checkout, ItemGroup, Item


class ModelsTestCase(TestCase):
    def test_models(self):
        self.assertEqual(True, False)
