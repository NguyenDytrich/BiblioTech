from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.shortcuts import redirect, render

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
            return redirect("itemgroup-list")
    else:
        form = LoginForm()

    return render(request, "equilizer/login.html", {"form": form***REMOVED***)
