from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from library.models import Item

class DenyCheckoutForm(forms.Form):
    reason = forms.CharField(label="Reason for Denial", max_length=500)


class ReturnCheckoutForm(forms.Form):
    checkout_id = forms.IntegerField()
    is_verified = forms.BooleanField()
    return_condition = forms.ChoiceField(choices=Item.Condition.choices)
    inspection_notes = forms.CharField(required=False)


class AddItemForm(forms.Form):
    make = forms.CharField()
    model = forms.CharField()
    moniker = forms.CharField(required=False)
    description = forms.CharField()


# TODO: might need to swap holding & items
class AddHoldingForm(forms.Form):
    itemgroup_id = forms.IntegerField()
    is_verified = forms.BooleanField()
    library_id = forms.SlugField()
    serial_num = forms.CharField()
    availability = forms.ChoiceField(choices=Item.Availability.choices)
    condition = forms.ChoiceField(choices=Item.Condition.choices)
    notes = forms.CharField(required=False)


class UpdateItemForm(forms.Form):
    availability = forms.ChoiceField(choices=Item.Availability.choices)
    condition = forms.ChoiceField(choices=Item.Condition.choices)
    notes = forms.CharField(required=False)


class DeleteItemForm(forms.Form):
    item_id = forms.IntegerField()
    item_name = forms.CharField()
    is_sure = forms.BooleanField()

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get("item_name")
        item_id = cleaned_data.get("item_id")
        if data and item_id:
            if data != str(Item.objects.get(pk=item_id)):
                self.add_error(
                    "item_name",
                    ValidationError(
                        _("This field must match the item identifier above!")
                    ),
                )
