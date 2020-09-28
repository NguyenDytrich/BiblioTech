from django.utils import timezone
from equilizer.models import Checkout, Item

from equilizer.validators import ItemValidator


def checkout_items(items, due_date, checkout_date=None, approval_status=None):
    ***REMOVED***
    Create a checkout entry for each of the set of items, validate that those items are
    avaialble, and then mark those items as checked out

    :param items: The items to checkout
    :type item: List, QuerySet, Item

    :param due_date: Date that items are due
    :type due_date: datetime

    :param checkout_date: checkout date, defaults to the current datetime
    :type checkout_date: datetime, optional

    :param approval_status: the approval status of the requested checkout, defaults to 'PENDING'
    :type approval_status: str, optional
    ***REMOVED***

    checkout_list = [***REMOVED***

    # If the items argument is just a single item
    # e.g. acquired via Item.objets.get(), then put
    # it into an array
    if isinstance(items, Item):
        items = [items***REMOVED***

    for item in items:
        # Check if our items are available before preceeding
        ItemValidator.is_available(item)

        # Set the availability
        item.availability = "CHECKED_OUT"
        item.save()

        checkout = Checkout.objects.create(item=item, due_date=due_date)
        if checkout_date:
            checkout.checkout_date = checkout_date
        if approval_status:
            checkout.approval_status = approval_status

        checkout.clean()
        checkout.save()
        checkout_list.append(checkout)

    # Validate the entry
    # Save the entry and return it
    return checkout_list


def return_items(checkout, return_date=None):
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
    # Validate the return date before making changes
    checkout.clean()

    # Then, mark items as returned
    item = checkout.item
    item.availability = "AVAILABLE"
    item.save()

    # Validate and save
    checkout.save()
    return checkout


def retrieve_items(cart):
    ***REMOVED***
    Retrieve a list of items from the inventory according to the entries in
    the cart.

    :param cart: A dictionary that represents the PK of the type of Item we want to checkout and
        its quantity
    :type cart: Dict
    ***REMOVED***
    item_list = [***REMOVED***
    # For each entry in our cart
    for item, qty in cart.items():
        # Append each available item found into item_list
        for i in Item.objects.filter(item_group_id=int(item), availability="AVAILABLE")[:qty***REMOVED***:
            item_list.append(i)

    return item_list
