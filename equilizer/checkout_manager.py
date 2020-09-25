from django.utils import timezone
from equilizer.models import Checkout, Item

from equilizer.validators import ItemValidator

item_validator = ItemValidator()


def checkout_items(items, due_date, checkout_date=None, approval_status=None):
    ***REMOVED***
    Create a checkout entry for the set of items, validate that those items are
    avaialble, and then mark those items as checked out

    :param items: The items to checkout
    :type item: List, QuerySet, Item

    :param due_date: Date that items are due
    :param type: datetime

    :param checkout_date: checkout date, defaults to the current datetime
    :param type: datetime, optional

    :param approval_status: the approval status of the requested checkout, defaults to 'PENDING'
    :param type: str, optional
    ***REMOVED***

    checkout = Checkout.objects.create(due_date=due_date)
    if checkout_date:
        checkout.checkout_date = checkout_date
    if approval_status:
        checkout.approval_status = approval_status

    # If the items argument is just a single item
    # e.g. acquired via Item.objets.get(), then put
    # it into an array
    if isinstance(items, Item):
        items = [items***REMOVED***

    for item in items:
        # Check if our items are available before preceeding
        item_validator.is_available(item)

        # First add the itme to checkout
        checkout.items.add(item)

        # Set the availability
        item.availability = "CHECKED_OUT"
        item.save()

    # Validate the entry
    checkout.clean()
    # Save the entry and return it
    checkout.save()
    return checkout


def return_items(checkout, items=None, return_date=None):
    ***REMOVED***
    Update a checkout entry, setting the items specified to AVAILABLE

    :param checkout: The checkout entry to update
    :type checkout: Checkout

    :param items: The items to return, defaults to all items
    :type item: List, QuerySet, Item, optional

    :param return_date: Date that items are returned, defaults to current datetime
    :param type: datetime
    ***REMOVED***
    # First, assign a return date
    if return_date:
        checkout.return_date = return_date
    else:
        checkout.return_date = timezone.now()

    # Then, mark items as returned
    if not items:
        items = checkout.items.get_all()

    for item in items:
        item.availability = "AVAILABLE"
        item.save()

    # Validate and save
    checkout.clean()
    checkout.save()
    return checkout
