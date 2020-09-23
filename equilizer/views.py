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
