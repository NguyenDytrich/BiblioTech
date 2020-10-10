from django import forms
from django.utils.translation import gettext_lazy as _

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
