from django.http import HttpResponseNotFound
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect
from django.urls import reverse

from library.models import Tag, ItemGroup
from management.forms import AddTagForm


class ItemGroupTagView(SingleObjectMixin, View):

    model = Tag


class ItemGroupTagListView(SingleObjectMixin, View):

    model = ItemGroup

    def post(self, request, *args, **kwargs):
        """
        Create a relationship between an itemgroup and a tag
        """
        form = AddTagForm(request.POST)
        valid = form.is_valid()

        if valid:
            data = form.cleaned_data
            item_group = self.get_object()
            tag, created = Tag.objects.get_or_create(name=data.get("tag_name").lower())

            if created:
                tag.display_name = data.get("tag_name")
                tag.save()

            # If the item is already tagged with the tag, skip this
            # unless the tag has just been created, in which case there
            # is no way the item could have this tag.
            if not tag in item_group.tags.all() or created:
                item_group.tags.add(tag)
                item_group.save()

            return redirect(
                request.POST.get(
                    "next", f"{reverse('master-inventory')}?active={item_group.id}"
                )
            )
        else:
            return HttpResponseNotFound()
