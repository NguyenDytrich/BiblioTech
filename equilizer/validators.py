from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


class ItemValidator:
    def is_available(self, item):
        if item.availability != "AVAILABLE":
            raise ValidationError(
                _("%(item) is not AVAIALABLE"),
                params={"item": item***REMOVED***,
            )


class MemberValidator:
    def member_id(value):
        id_regex = re.compile(r"^\d{6***REMOVED***$", flags=re.M)
        if re.match(id_regex, value) is None:
            raise ValidationError("member ID should be 6 digits.")

class CartValidator:
    def has_inventory(itemgroup):
        pass
