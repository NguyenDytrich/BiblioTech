from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


class AgreedToTerms(forms.Form):
    agreed = forms.BooleanField()
