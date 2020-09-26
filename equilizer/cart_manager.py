def add_to_cart(cart, itemgroup_id):
    ig_id = str(itemgroup_id)
    if isinstance(cart, dict):
        new_val = cart.get(ig_id, 0) + 1
        cart[ig_id***REMOVED*** = new_val
    else:
        raise TypeError("Expected `cart` to be Dict but found %s" % type(cart))
