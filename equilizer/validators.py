from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ItemValidator:
    def is_available(self, item):
        if item.availability != "AVAILABLE":
            raise ValidationError(
                _("%(item) is not AVAIALABLE"),
                params={"item": item***REMOVED***,
            )


class CheckoutValidator:
    def return_is_before_checkout(self, checkout):
        if checkout.due_date < checkout.checkout_date:
            raise ValidationError(
                _("%(checkout) cannot have due date before checkout date"),
                params={"checkout": checkout***REMOVED***,
            )
