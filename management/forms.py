from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from library.models import Item


class DenyCheckoutForm(forms.Form):
    reason = forms.CharField(label="Reason for Denial", max_length=500)

class AddTagForm(forms.Form):
    tag_name = forms.CharField(max_length=500)


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
    default_checkout_len = forms.IntegerField()


# TODO: might need to swap holding & items
class AddHoldingForm(forms.Form):
    itemgroup_id = forms.IntegerField()
    is_verified = forms.BooleanField()
    library_id = forms.SlugField()
    serial_num = forms.CharField()
    availability = forms.ChoiceField(choices=Item.Availability.choices)
    condition = forms.ChoiceField(choices=Item.Condition.choices)
    notes = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        lid = cleaned_data.get("library_id")
        if lid:
            if Item.objects.filter(library_id=lid).count() > 0:
                self.add_error(
                    "library_id",
                    ValidationError(_(f"Library id {lid} already in system!")),
                )

        sn = cleaned_data.get("serial_num")
        ig = cleaned_data.get("itemgroup_id")
        if sn:
            if Item.objects.filter(item_group_id=ig, serial_num=sn).count() > 0:
                self.add_error(
                    "library_id",
                    ValidationError(
                        _(f"Serial number {sn} already in system!")
                    ),
                )


class UpdateItemForm(forms.Form):
    availability = forms.ChoiceField(choices=Item.Availability.choices)
    condition = forms.ChoiceField(choices=Item.Condition.choices)
    notes = forms.CharField(required=False)

class UpdateItemGroupForm(forms.Form):
    description = forms.CharField(required=False)
    features = forms.CharField(required=False)
    external_resources = forms.CharField(required=False)


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
