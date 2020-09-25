from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ItemValidator:
    def is_available(self, item):
        if item.availability != "AVAILABLE":
            raise ValidationError(
                _("%(item) is not AVAIALABLE"),
                params={"item": item***REMOVED***,
            )
