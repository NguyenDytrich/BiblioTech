from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class ItemGroup(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)


class Item(models.Model):
    # Protect prevents an ItemGroup with referenced items from being deleted
    # automatically in a CASCADE.
    item_group = models.ForeignKey(ItemGroup, on_delete=models.PROTECT)


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
