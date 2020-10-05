from django.test import TestCase
from parameterized import parameterized

from bibliotech.forms import *


class LoginFormTests(TestCase):
    @parameterized.expand(
        [
            ({"username": "username", "password": "password"}, true),
            ({"username": "", "password": ""}, false),
        ]
    )
    def test_validation(self, info_dict, validity):
        form = LoginForm(info_dict)
        self.assertEqual(form.is_valid(), validity)


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


class AgreedToTerms(TestCase):
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


class ReturnCheckoutForm(forms.Form):
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
