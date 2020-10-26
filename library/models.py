from datetime import timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import pytz

from library.validators import MemberValidator

tz = pytz.timezone("UTC")

member_validator = MemberValidator


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member_id = models.CharField(
        max_length=6, unique=True, validators=[member_validator.member_id]
    )


class Tag(models.Model):
    # TODO: Hold off on subtags until a later stage in development
    # parent_tag = models.ForeignKey('self')
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"<Tag {self.name}>"

    def save(self, *args, **kwargs):
        # Set display name as user-formatted value
        self.display_name = self.name

        # Normalize tag names to lowercase
        self.name = self.name.lower()
        return super(Tag, self).save(*args, **kwargs)


class ItemGroup(models.Model):
    moniker = models.CharField(max_length=100, null=True, blank=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField()
    features = models.TextField(null=True, blank=True)
    external_resources = models.TextField(null=True, blank=True)
    default_checkout_len = models.IntegerField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        if self.moniker:
            return self.moniker
        else:
            return f"{self.make} {self.model}"

    @property
    def default_return_date(self):
        return timezone.now() + timedelta(self.default_checkout_len)

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

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["item_group", "serial_num"], name="unique_itemgroup_member"
            )
        ]

    # Protect prevents an ItemGroup with referenced items from being deleted
    # automatically in a CASCADE.
    item_group = models.ForeignKey(ItemGroup, on_delete=models.PROTECT)
    library_id = models.SlugField(max_length=20, unique=True)
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
            return f"{str(self.item_group)} sn. {self.serial_num}"

    def make_model_sn(self):
        """
        Get the make/model and serial number of the item
        """
        return f"{self.item_group.make} {self.item_group.model} sn. {self.serial_num}"


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

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    approver = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="approver_id",
        blank=True,
        null=True,
    )
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
        return f"{str(self.item)}"
