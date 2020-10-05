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


# TODO: you can access this page from wherever, whenever
def success(request):
    """
    Catch all success page
    """
    return render(request, "bibliotech/success.html")
