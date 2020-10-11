from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.Form):
    fname = forms.CharField()
    lname = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    password_confirm = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        pwd_conf = cleaned_data.get("password_confirm")
        if pwd and pwd_conf:
            if pwd != pwd_conf:
                self.add_error(
                    "password_confirm",
                    ValidationError(_("Passwords don't match!")),
                )
