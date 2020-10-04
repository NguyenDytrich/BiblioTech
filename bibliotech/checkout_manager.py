from django.utils import timezone

from bibliotech.models import Checkout, Item
from bibliotech.validators import ItemValidator


def checkout_items(items, due_date, user, checkout_date=None, approval_status=None):
    """
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
    """

    checkout_list = []

    # If the items argument is just a single item
    # e.g. acquired via Item.objets.get(), then put
    # it into an array
    if isinstance(items, Item):
        items = [items]

    for item in items:
        # Check if our items are available before preceeding
        ItemValidator.is_available(item)

        # Set the availability
        item.availability = "CHECKED_OUT"
        item.save()

        checkout = Checkout.objects.create(item=item, due_date=due_date, user=user)
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


# TODO: don't set condition to none
def return_items(checkout, condition=None, notes=None, return_date=None):
    """
    Update a checkout entry, setting the items specified to AVAILABLE

    :param checkout: The checkout entry to update
    :type checkout: Checkout

    :param items: The items to return, defaults to all items
    :type item: List, QuerySet, Item, optional

    :param return_date: Date that items are returned, defaults to current datetime
    :param type: datetime
    """
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
    if condition:
        item.condition = condition
    item.save()

    # Validate and save
    checkout.save()
    return checkout


def retrieve_items(cart):
    """
    Retrieve a list of items from the inventory according to the entries in
    the cart.

    :param cart: A dictionary that represents the PK of the type of Item we want to checkout and
        its quantity
    :type cart: Dict
    """
    item_list = []
    # For each entry in our cart
    for item, qty in cart.items():
        # Append each available item found into item_list
        for i in Item.objects.filter(item_group_id=int(item), availability="AVAILABLE")[
            :qty
        ]:
            item_list.append(i)

    return item_list


def approve_checkout(checkout):
    """
    Set the approval status of the passed checkout as "APPROVED".

    :param checkout: Checkout entry to approve
    :type checkout: Checkout
    """
    checkout.approval_status = "APPROVED"
    checkout.clean()

    checkout.save()


def deny_checkout(checkout):
    """
    Set the approval status of the passed checkout as "DENIED", and set the availability of
    the item as "AVAILABLE"

    :param checkout: Checkout entry to deny
    :type checkout: Checkout
    """
    item = checkout.item

    checkout.approval_status = "DENIED"
    checkout.checkout_status = "RETURNED"
    item.availability = "AVAILABLE"

    checkout.clean()
    item.clean()

    checkout.save()
    item.save()
