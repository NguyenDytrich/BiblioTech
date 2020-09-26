from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import pytz

from equilizer.validators import MemberValidator

tz = pytz.timezone("UTC")

member_validator = MemberValidator


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member_id = models.CharField(
        max_length=6, unique=True, validators=[member_validator.member_id***REMOVED***
    )


class ItemGroup(models.Model):
    moniker = models.CharField(max_length=100, null=True, blank=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        if self.moniker:
            return self.moniker
        else:
            return f"{self.make***REMOVED*** {self.model***REMOVED***"

    def total_inventory(self):
        return len(self.item_set.all())

    def avail_inventory(self):
        return len(self.avail_items())

    def avail_items(self):
        return self.item_set.filter(availability="AVAILABLE")


class Item(models.Model):
    class Availability(models.TextChoices):
        AVAILABLE = "AVAILABLE", _("Available")
        HOLD = "HOLD", _("Hold")
        UNAVAILABLE = "UNAVAILABLE", _("Unavailable")
        CHECKED_OUT = "CHECKED_OUT", _("Checked out")
        LOST = "LOST", _("Lost")

    class Condition(models.TextChoices):
        BROKEN = "BROKEN", _("Broken")
        POOR = "POOR", _("Poor")
        FAIR = "FAIR", _("Fair")
        GOOD = "GOOD", _("Good")
        EXCELLENT = "EXCELLENT", _("Excellent")

    # Protect prevents an ItemGroup with referenced items from being deleted
    # automatically in a CASCADE.
    item_group = models.ForeignKey(ItemGroup, on_delete=models.PROTECT)
    library_id = models.CharField(max_length=20, unique=True)
    serial_num = models.CharField(max_length=100)
    availability = models.CharField(
        max_length=15, choices=Availability.choices, default=Availability.AVAILABLE
    )
    date_acquired = models.DateField(default=timezone.now(), blank=True)
    last_inspected = models.DateTimeField(default=timezone.now(), blank=True)
    condition = models.CharField(
        max_length=15, choices=Condition.choices, default=Condition.FAIR
    )
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.library_id:
            return self.library_id
        else:
            return f"{str(self.item_group)***REMOVED*** sn. {self.serial_num***REMOVED***"

    def make_model_sn(self):
        ***REMOVED***
        Get the make/model and serial number of the item
        ***REMOVED***
        return f"{self.item_group.make***REMOVED*** {self.item_group.model***REMOVED*** sn. {self.serial_num***REMOVED***"


class Checkout(models.Model):
    class ApprovalStatus(models.TextChoices):
        APPROVED = "APPROVED", _("Approved")
        PENDING = "PENDING", _("Pending")
        DENIED = "DENIED", _("Denied")

    class CheckoutStatus(models.TextChoices):
        RETURNED = "RETURNED", _("Returned")
        OVERDUE = "OVERDUE", _("Overdue")
        LOST = "LOST", _("Lost")
        OUTSTANDING = "OUTSTANDING", _("Outstanding")

    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    checkout_date = models.DateTimeField(default=timezone.now(), blank=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
    approval_status = models.CharField(
        max_length=15,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
        blank=True,
    )
    checkout_status = models.CharField(
        max_length=15,
        choices=CheckoutStatus.choices,
        default=CheckoutStatus.OUTSTANDING,
    )

    def clean(self):
        if self.due_date < self.checkout_date:
            raise ValidationError(_("Due date cannot be before checkout date."))
        if self.return_date:
            if self.return_date < self.checkout_date:
                raise ValidationError(_("Return date cannot be before checkout date."))

    def __str__(self):
        return str(self.checkout_date)
