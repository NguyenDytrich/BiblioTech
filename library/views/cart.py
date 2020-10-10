from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

import library.cart_manager as cart_manager
from library.models import ItemGroup

def cart_view(request):
    empty_cart = False
    cart_items = []

    cart = request.session.get("cart")
    if cart and sum(cart.values()) > 0:
        cart_items = cart_manager.retrieve_for_display(request.session["cart"])
    else:
        empty_cart = True

    return render(
        request,
        "library/cart.html",
        {"cart_items": cart_items, "empty_cart": empty_cart},
    )

@login_required(login_url="/login", redirect_field_name=None)
def add_to_cart(request, itemgroup_id):

    # Redirect to the item page if it's not a post request
    if request.method == "GET":
        return redirect(reverse("itemgroup-detail", args=(itemgroup_id,)))

    item = get_object_or_404(ItemGroup, pk=itemgroup_id)

    if "cart" not in request.session:
        request.session["cart"] = dict()

    cart = request.session["cart"]

    try:
        cart_manager.add_to_cart(cart, item.id)
        request.session["cart_sum"] = sum(cart.values())
        messages.success(request, f"{item} successfully added to cart.")
    except ValidationError:
        messages.error(request, f"All available {item}s are already in your cart!")

    detail_view = reverse("itemgroup-detail", args=(item.id,))

    return redirect(request.POST.get("return", detail_view))

