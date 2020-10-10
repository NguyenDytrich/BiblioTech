from .models import ItemGroup
from .validators import CartValidator as validator


def add_to_cart(cart, itemgroup_id, count=1):
    """
    Adds an item to a Dict representing our cart.

    :param cart: the dictionary representing our cart
    :type cart: Dict

    :param itemgroup_id: the id of the item to add
    :type itemgroup_id: int

    :param count: the number of items to add, defaults to 1
    :type count: int, optional
    """
    ig_id = str(itemgroup_id)
    if not isinstance(cart, dict):
        raise TypeError("Expected `cart` to be Dict but found %s" % type(cart))

    item = ItemGroup.objects.get(pk=itemgroup_id)

    # Validate that the item has the inventory to fulfill a checkout request
    # TODO: return specialized errors
    validator.has_inventory(item)
    validator.does_not_exceed(cart, item)
    new_val = cart.get(ig_id, 0) + count
    cart[ig_id] = new_val


def retrieve_for_display(cart):
    """
    Retrieves displayable information in dictionary format
    """
    dto = []
    for key, val in cart.items():
        itemgroup = ItemGroup.objects.get(pk=key)
        dto.append({"name": str(itemgroup), "quantity": val})
    return dto
