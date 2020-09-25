from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import ItemGroup


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
    username = request.POST["username"***REMOVED***
    password = request.POST["password"***REMOVED***
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Nav to success page
    else:
        # Return invalid error msg
        pass
