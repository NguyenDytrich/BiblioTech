from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_item_available(item):
    if item.availability is not "AVAILABLE":
        raise ValidationError(
            _("%(item) is not AVAIALABLE"),
            params={"item": item***REMOVED***,
        )
