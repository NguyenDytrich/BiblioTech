from django.test import TestCase
from parameterized import parameterized

from management.forms import *


class DenyCheckoutFormTests(TestCase):
    @parameterized.expand(
        [
            ({"reason": "reason"}, True),
            ({"reason": ""}, False),
        ]
    )
    def test_validation(self, info_dict, validity):
        form = DenyCheckoutForm(info_dict)
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
                True,
            ),
            (
                {
                    "checkout_id": "",
                    "is_verified": "",
                    "return_condition": "",
                    "inspection_notes": "",
                },
                False,
            ),
            (
                {
                    "checkout_id": "0",
                    "is_verified": "FALSE",
                    "return_condition": "GOOD",
                    "inspection_notes": "",
                },
                False,
            ),
            (
                {
                    "checkout_id": "0",
                    "is_verified": "",
                    "return_condition": "GOOD",
                    "inspection_notes": "",
                },
                False,
            ),
            (
                {
                    "checkout_id": "0",
                    "is_verified": "TRUE",
                    "return_condition": "notgood",
                    "inspection_notes": "",
                },
                False,
            ),
        ]
    )
    def test_validation(self, info_dict, validity):
        form = ReturnCheckoutForm(info_dict)
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
                    "default_checkout_len": 7,
                },
                True,
            ),
            (
                {
                    "make": "",
                    "model": "",
                    "moniker": "",
                    "description": "",
                },
                False,
            ),
            (
                {
                    "make": "Shure",
                    "model": "SM57",
                    "moniker": "",
                    "description": "A microphone",
                    "default_checkout_len": 7,
                },
                True,
            ),
        ]
    )
    def test_validation(self, info_dict, validity):
        form = AddItemForm(info_dict)
        self.assertEqual(form.is_valid(), validity)
