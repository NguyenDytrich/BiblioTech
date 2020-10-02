from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import ItemGroup, Checkout
from .forms import LoginForm, DenyCheckoutForm
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
        queryset = queryset.filter(user=self.request.user)
        return queryset


def home_view(request):
    return render(request, "equilizer/home.html")


def cart_view(request):
    empty_cart = False
    cart_items = [***REMOVED***

    cart = request.session.get("cart")
    if cart and sum(cart.values()) > 0:
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
        else:
            # Return to login page
            # TODO: Display some errors
            return render(request, "equilizer/login.html")
    # Redirect to home if the user is logged in already
    elif request.user.is_authenticated:
        return redirect("itemgroup-list")
    else:
        # I don't think this actually does anything anymore...
        form = LoginForm()
        return render(request, "equilizer/login.html", {"form": form***REMOVED***)


@require_http_methods(["POST"***REMOVED***)
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    # Redirect to value specified by 'return' otherwise, redirect to th list view
    return redirect(request.POST.get("next", "home"))


@login_required(login_url="/login", redirect_field_name=None)
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
@login_required(login_url="/login", redirect_field_name=None)
def create_checkout(request):
    if not "cart" in request.session or not request.user.is_authenticated:
        return HttpResponseBadRequest()
    try:
        item_list = checkout_manager.retrieve_items(request.session["cart"***REMOVED***)
        # TODO: Hey right now this defaults to 4 days but you probably don't wanna do this
        checkout_manager.checkout_items(
            item_list, timezone.now() + timedelta(4), request.user
        )

        # Retrieve the session and set the cart to an empty dict.
        session = request.session
        session["cart"***REMOVED*** = dict()
        session.save()

        return redirect(reverse("success-view"))
    except ValidationError:
        return HttpResponseBadRequest()


def success(request):
    ***REMOVED***
    Catch all success page
    ***REMOVED***
    return render(request, "equilizer/success.html")


# This is an unrelated method
def librarian_check(user):
    return user.groups.filter(name="librarian").exists()


@require_http_methods(["POST"***REMOVED***)
def approve_checkout(request, checkout_id):
    ***REMOVED***
    Mark the checkout as approved
    ***REMOVED***
    user = request.user
    # Manually check to see if the user passes all tests
    # TODO: maybe cleaner way to do this?
    if user.is_authenticated and librarian_check(user):
        checkout = Checkout.objects.get(pk=checkout_id)
        checkout_manager.approve_checkout(checkout)
        return redirect(request.POST.get("return", "librarian-control-panel"))
    # Otherwise raise PermissionDenied, which redirects to a 403 page
    else:
        raise PermissionDenied


class DenyCheckoutView(LoginRequiredMixin, UserPassesTestMixin, View):
    raise_exception = True

    def test_func(self):
        ***REMOVED***
        Test the user is part of the librarian group
        ***REMOVED***
        return librarian_check(self.request.user)

    def get(self, request, checkout_id):
        ***REMOVED***
        Display a form to provide a reason for checkout denial
        ***REMOVED***
        checkout = Checkout.objects.get(pk=checkout_id)
        if checkout.approval_status != "PENDING":
            return HttpResponseBadRequest()
        else:
            return render(
                request,
                "equilizer/deny_checkout.html",
            ***REMOVED***"checkout_id": checkout_id, "form": DenyCheckoutForm()***REMOVED***,
            )

    def post(self, request, checkout_id):
        ***REMOVED***
        Mark the checkout as denied, and the item as available
        ***REMOVED***
        form = DenyCheckoutForm(request.POST)
        is_valid = form.is_valid()

        checkout = Checkout.objects.get(pk=checkout_id)

        if not is_valid:
            return render(
                request,
                "equilizer/deny_checkout.html",
            ***REMOVED***"checkout_id": checkout_id, "form": form***REMOVED***,
            )

        else:
            # TODO: implement an audit log of denied checkouts
            reason = form.cleaned_data.get("reason")
            checkout_manager.deny_checkout(checkout)
            return redirect(reverse("librarian-control-panel"))
