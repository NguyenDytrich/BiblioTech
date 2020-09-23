from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


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
    library_id = models.CharField(max_length=20)
    serial_num = models.CharField(max_length=100)
    availability = models.CharField(
        max_length=15, choices=Availability.choices, default=Availability.AVAILABLE
    )
    date_acquired = models.DateTimeField(default=timezone.now(), blank=True)
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

    items = models.ManyToManyField(Item)
    checkout_date = models.DateTimeField(default=timezone.now(), blank=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
    approval_status = models.CharField(
        max_length=15,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
    )
    checkout_status = models.CharField(
        max_length=15,
        choices=CheckoutStatus.choices,
        default=CheckoutStatus.OUTSTANDING,
    )

    def __str__(self):
        return str(self.checkout_date)
