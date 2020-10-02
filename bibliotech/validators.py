from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


class ItemValidator:
    @staticmethod
    def is_available(item):
        if item.availability != "AVAILABLE":
            raise ValidationError(
                _("%(item) is not AVAIALABLE"),
                params={"item": item***REMOVED***,
            )


class MemberValidator:
    @staticmethod
    def member_id(value):
        ***REMOVED***
        Validate that member IDs only allow 6-digit strings
        ***REMOVED***
        id_regex = re.compile(r"^\d{6***REMOVED***$", flags=re.M)
        if re.match(id_regex, value) is None:
            raise ValidationError(_("Member ID should be 6 digits."))


class CartValidator:
    @staticmethod
    def has_inventory(itemgroup):
        ***REMOVED***
        Validate that the itemgroup has an available Item to checkout
        ***REMOVED***
        if itemgroup.avail_inventory() < 1:
            raise ValidationError(
                _("Out of inventory for item %(group)"), params={"group": itemgroup***REMOVED***
            )

    @staticmethod
    def does_not_exceed(cart, itemgroup, count=1):
        ***REMOVED***
        Validate that adding to the inventory does not exceed available inventory

        :param cart: the Dict representing the cart
        :type cart: Dict

        :param itemgroup: the item group to add
        :type itemgroup: ItemGroup

        :param count: number of items to add, defaults to 1
        :type  count: Int, optional
        ***REMOVED***
        str_id = str(itemgroup.id)
        # Return if the itemgroup is not in the cart
        if not str_id in cart:
            return

        current_count = cart[str_id***REMOVED***
        if (current_count + count) > itemgroup.avail_inventory():
            raise ValidationError(
                _("Not enough %(group)s available to checkout %(count) item(s)."),
                params={"group": itemgroup, "count": count***REMOVED***,
            )
