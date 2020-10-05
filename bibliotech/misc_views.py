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
from .forms import LoginForm, DenyCheckoutForm, AgreedToTerms
import bibliotech.cart_manager as cart_manager
import bibliotech.checkout_manager as checkout_manager


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
        queryset = queryset.filter(user=self.request.user).order_by("-checkout_date")
        return queryset


def home_view(request):
    return render(request, "bibliotech/home.html")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        form.is_valid()

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Nav to success page
            return redirect(request.POST.get("next", "itemgroup-list"))
        else:
            # Return to login page
            # TODO: Display some errors
            return render(request, "bibliotech/login.html")
    # Redirect to home if the user is logged in already
    elif request.user.is_authenticated:
        return redirect("itemgroup-list")
    else:
        # I don't think this actually does anything anymore...
        form = LoginForm()
        return render(request, "bibliotech/login.html", {"form": form})


@require_http_methods(["POST"])
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    # Redirect to value specified by 'return' otherwise, redirect to th list view
    return redirect(request.POST.get("next", "home"))


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


# TODO: you can access this page from wherever, whenever
def success(request):
    """
    Catch all success page
    """
    return render(request, "bibliotech/success.html")


# This is an unrelated method
def librarian_check(user):
    return user.groups.filter(name="librarian").exists()


@require_http_methods(["POST"])
def approve_checkout(request, checkout_id):
    """
    Mark the checkout as approved
    """
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
