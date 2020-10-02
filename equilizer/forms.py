from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

class DenyCheckoutForm(forms.Form):
    reason = forms.CharField(label="Reason for Denial", max_length=500)
