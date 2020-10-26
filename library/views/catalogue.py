from django.views import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView

from library.models import ItemGroup, Tag

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

class ItemGroupTagView(SingleObjectMixin, View):

    model = Tag
