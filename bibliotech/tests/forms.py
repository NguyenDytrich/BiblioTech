from bibliotech.forms import LoginForm


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
