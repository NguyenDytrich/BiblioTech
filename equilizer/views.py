from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404

from .models import ItemGroup
from .forms import LoginForm


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

    cart[str(item.id)***REMOVED*** = cart.get(str(item.id), 0) + 1
    print(cart)
    request.session["cart_sum"***REMOVED*** = sum(cart.values())

    return redirect(reverse("itemgroup-detail", args=(item.id,)))
