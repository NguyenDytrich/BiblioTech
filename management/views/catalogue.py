from django.views import View
from django.views.generic.detail import SingleObjectMixin

from library.models import Tag, ItemGroup


class ItemGroupTagView(SingleObjectMixin, View):

    model = Tag


class ItemGroupTagListView(View):
    def post(self, pk, *args, **kwargs):
        """
        Create a relationship between an itemgroup and a tag
        """
        item_group = ItemGroup.get(pk=pk)
