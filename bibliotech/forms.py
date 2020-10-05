from django import forms

from bibliotech.models import Item


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

class DenyCheckoutForm(forms.Form):
    reason = forms.CharField(label="Reason for Denial", max_length=500)

class AgreedToTerms(forms.Form):
    agreed = forms.BooleanField()

class ReturnCheckoutForm(forms.Form):
    checkout_id = forms.IntegerField()
    is_verified = forms.BooleanField()
    return_condition = forms.ChoiceField(choices=Item.Condition.choices)
    inspection_notes = forms.CharField(required=False)
