from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import ItemGroup, Checkout
from .forms import LoginForm
import equilizer.cart_manager as cart_manager
import equilizer.checkout_manager as checkout_manager


class ItemGroupListView(ListView):

    model = ItemGroup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ItemGroupDetailView(DetailView):

    model = ItemGroup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CheckoutListView(ListView):
    model = Checkout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = super(CheckoutListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


def cart_view(request):
    empty_cart = False
    cart_items = [***REMOVED***

    if "cart" in request.session:
        cart_items = cart_manager.retrieve_for_display(request.session["cart"***REMOVED***)
    else:
        empty_cart = True

    return render(
        request,
        "equilizer/cart.html",
    ***REMOVED***"cart_items": cart_items, "empty_cart": empty_cart***REMOVED***,
    )


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        form.is_valid()

        username = form.cleaned_data["username"***REMOVED***
        password = form.cleaned_data["password"***REMOVED***

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Nav to success page
            return redirect(request.POST.get("next", "itemgroup-list"))
    # Redirect to home if the user is logged in already
    elif request.user.is_authenticated:
        return redirect("itemgroup-list")
    else:
        form = LoginForm()
        return render(request, "equilizer/login.html", {"form": form***REMOVED***)


@login_required(login_url="/login")
def add_to_cart(request, itemgroup_id):

    # Redirect to the item page if it's not a post request
    if request.method == "GET":
        return redirect(reverse("itemgroup-detail", args=(itemgroup_id,)))

    item = get_object_or_404(ItemGroup, pk=itemgroup_id)

    if "cart" not in request.session:
        request.session["cart"***REMOVED*** = dict()

    cart = request.session["cart"***REMOVED***

    try:
        cart_manager.add_to_cart(cart, item.id)
        request.session["cart_sum"***REMOVED*** = sum(cart.values())
    except ValidationError:
        messages.error(request, "All available items are already in your cart!")

    detail_view = reverse("itemgroup-detail", args=(item.id,))

    return redirect(request.POST.get("return", detail_view))


@require_http_methods(["POST"***REMOVED***)
@login_required(login_url="/login")
def create_checkout(request):
    if not "cart" in request.session or not request.user.is_authenticated:
        return HttpResponseBadRequest()
    try:
        item_list = checkout_manager.retrieve_items(request.session["cart"***REMOVED***)
        # TODO: Hey right now this defaults to 4 days but you probably don't wanna do this
        checkout_manager.checkout_items(
            item_list, timezone.now() + timedelta(4), request.user
        )
        return redirect(reverse("success-view"))
    except ValidationError:
        return HttpResponseBadRequest()


def success(request):
    ***REMOVED***
    Catch all success page
    ***REMOVED***
    return render(request, "equilizer/success.html")
