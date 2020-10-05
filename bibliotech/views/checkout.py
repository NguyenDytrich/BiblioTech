from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView

import bibliotech.cart_manager as cart_manager
import bibliotech.checkout_manager as checkout_manager
from bibliotech.forms import AgreedToTerms
from bibliotech.models import Checkout


class CheckoutListView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = None
    model = Checkout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # TODO: Test this
    def get_queryset(self):
        queryset = super(CheckoutListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by("-checkout_date")
        return queryset


@require_http_methods(["POST"])
@login_required(login_url="/login", redirect_field_name=None)
def create_checkout(request):

    if not "cart" in request.session or not request.user.is_authenticated:
        return HttpResponseBadRequest()

    form = AgreedToTerms(request.POST)
    form.is_valid()
    agreed = form.cleaned_data.get("agreed")

    cart_items = cart_manager.retrieve_for_display(request.session["cart"])

    if not agreed:
        return render(
            request,
            "bibliotech/cart.html",
            # Probably not wise to set to false here, but logically speaking
            # This form isn't accessible unless there is a cart available anyway
            {"cart_items": cart_items, "empty_cart": False, "form": form},
        )

    try:
        item_list = checkout_manager.retrieve_items(request.session["cart"])
        # TODO: Hey right now this defaults to 4 days but you probably don't wanna do this
        checkout_manager.checkout_items(
            item_list, timezone.now() + timedelta(4), request.user
        )

        # Retrieve the session and set the cart to an empty dict.
        session = request.session
        session["cart"] = dict()
        session.save()

        return redirect(reverse("success-view"))
    except ValidationError:
        return HttpResponseBadRequest()
