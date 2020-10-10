from django.test import TestCase
from parameterized import parameterized

from library.forms import *


class DenyCheckoutFormTests(TestCase):
    @parameterized.expand(
        [
            ({"reason": "reason"}, true),
            ({"reason": ""}, false),
        ]
    )
    def test_validation(self, info_dict, validity):
        form = DenyCheckoutForm(info_dict)
        self.assertEqual(form.is_valid(), validity)


class AgreedToTermsTests(TestCase):
    @parameterized.expand(
        [
            ({"agreed": "TRUE"}, true),
            ({"agreed": "FALSE"}, false),
            ({"agreed": ""}, false),
        ]
    )
    def test_validation(self, info_dict, validity):
        form = AgreedToTerms(info_dict)
        self.assertEqual(form.is_valid(), validity)


class ReturnCheckoutFormTests(TestCase):
    @parameterized.expand(
        [
            (
                {
                    "checkout_id": "0",
                    "is_verified": "TRUE",
                    "return_condition": "GOOD",
                    "inspection_notes": "test",
                },
                true,
            ),
            (
                {
                    "checkout_id": "",
                    "is_verified": "",
                    "return_condition": "",
                    "inspection_notes": "",
                },
                false,
            ),
            (
                {
                    "checkout_id": "0",
                    "is_verified": "FALSE",
                    "return_condition": "GOOD",
                    "inspection_notes": "",
                },
                false,
            ),
            (
                {
                    "checkout_id": "0",
                    "is_verified": "",
                    "return_condition": "GOOD",
                    "inspection_notes": "",
                },
                false,
            ),
            (
                {
                    "checkout_id": "0",
                    "is_verified": "TRUE",
                    "return_condition": "notgood",
                    "inspection_notes": "",
                },
                false,
            ),
        ]
    )
    def test_validation(self, info_dict, validity):
        form = AgreedToTerms(info_dict)
        self.assertEqual(form.is_valid(), validity)


class AddItemFormTests(TestCase):
    @parameterized.expand(
        [
            (
                {
                    "make": "Shure",
                    "model": "SM57",
                    "moniker": "SM57",
                    "description": "A microphone",
                },
                true,
            ),
            (
                {
                    "make": "",
                    "model": "",
                    "moniker": "",
                    "description": "",
                },
                false,
            ),
            (
                {
                    "make": "Shure",
                    "model": "SM57",
                    "moniker": "",
                    "description": "A microphone",
                },
                false,
            ),
        ]
    )
    def test_validation(self, info_dict, validity):
        form = AgreedToTerms(info_dict)
        self.assertEqual(form.is_valid(), validity)
