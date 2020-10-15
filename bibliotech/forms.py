from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    # TODO: implement form errors on bad password
    def clean(self):
        cleaned_data = super().clean()
        user = None
        pwd = cleaned_data.get("password")
        try:
            user = User.objects.get(username=cleaned_data.get("username"))
        except User.DoesNotExist:
            raise ValidationError(_("Invalid username or password"))
        if user and pwd:
            if not user.check_password(pwd):
                raise ValidationError(_("Invalid username or password"))


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
            try:
                validate_password(pwd)
            except ValidationError as e:
                self.add_error("password", e)
            if pwd != pwd_conf:
                self.add_error(
                    "password_confirm",
                    ValidationError(_("Passwords don't match!")),
                )


class UpdateProfileForm(forms.Form):
    fname = forms.CharField()
    lname = forms.CharField()
    email = forms.EmailField()


class UpdatePasswordForm(forms.Form):
    user_id = forms.IntegerField()
    password = forms.CharField()
    new_password = forms.CharField()
    new_confirmed = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        user = User.objects.get(pk=cleaned_data.get("user_id"))
        current_pwd = cleaned_data.get("password")
        new_pwd = cleaned_data.get("new_password")
        new_conf = cleaned_data.get("new_confirmed")
        if user and current_pwd:
            # Check if the password matches the current user's password
            if not user.check_password(current_pwd):
                self.add_error("password", ValidationError(_("Incorrect password")))
        if new_pwd and new_conf:
            # Check if the password confirmation matches the new password
            if new_pwd != new_conf:
                self.add_error("new_confirmed", ValidationError(_("Passwords don't match!")))
