from django.test import TestCase
from parameterized import parameterized

from library.forms import *


class AgreedToTermsTests(TestCase):
    @parameterized.expand(
        [
            ({"agreed": "TRUE"}, True),
            ({"agreed": "FALSE"}, False),
            ({"agreed": ""}, False),
        ]
    )
    def test_validation(self, info_dict, validity):
        form = AgreedToTerms(info_dict)
        self.assertEqual(form.is_valid(), validity)
