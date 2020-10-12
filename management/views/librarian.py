from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.utils import timezone

from lxml.html import document_fromstring
from lxml.html.clean import Cleaner

from management.forms import (
    DenyCheckoutForm,
    ReturnCheckoutForm,
    AddItemForm,
    AddHoldingForm,
    UpdateItemForm,
    DeleteItemForm,
)
from library.models import Checkout, Item, ItemGroup
import library.checkout_manager as checkout_manager
import management.inventory_manager as inventory_manager


def librarian_check(user):
    return user.groups.filter(name="librarian").exists()


# TODO: refactor all librarian views to derive from this class
class LibrarianViewBase(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "/login/"
    redirect_field_name = None
    raise_exception = True

    def test_func(self):
        """
        Test the user is part of the librarian group
        """
        return librarian_check(self.request.user)


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


class LibrarianView(LibrarianViewBase, View):
    template_name = "management/librarian_control_panel.html"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {"pending_checkouts": self.get_pending_checkouts()},
        )

    @staticmethod
    def get_pending_checkouts():
        """
        Returns the queryset of pending checkouts ordered by oldest -> most recent
        """
        checkouts = Checkout.objects.filter(approval_status="PENDING").order_by(
            "checkout_date"
        )
        if len(checkouts) > 0:
            return checkouts
        else:
            return None


class DenyCheckoutView(LibrarianViewBase, View):
    def get(self, request, checkout_id):
        """
        Display a form to provide a reason for checkout denial
        """
        checkout = Checkout.objects.get(pk=checkout_id)
        if checkout.approval_status != "PENDING":
            return HttpResponseBadRequest()
        else:
            return render(
                request,
                "management/deny_checkout.html",
                {"checkout_id": checkout_id, "form": DenyCheckoutForm()},
            )

    def post(self, request, checkout_id):
        """
        Mark the checkout as denied, and the item as available
        """
        form = DenyCheckoutForm(request.POST)
        is_valid = form.is_valid()

        checkout = Checkout.objects.get(pk=checkout_id)

        if not is_valid:
            return render(
                request,
                "management/deny_checkout.html",
                {"checkout_id": checkout_id, "form": form},
            )

        else:
            # TODO: implement an audit log of denied checkouts
            reason = form.cleaned_data.get("reason")
            checkout_manager.deny_checkout(checkout)
            return redirect(reverse("librarian-control-panel"))


class MasterCheckoutListView(LibrarianViewBase, ListView):
    model = Checkout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # TODO: Test this
    def get_queryset(self):
        queryset = super(MasterCheckoutListView, self).get_queryset()
        queryset = queryset.filter(checkout_status="OUTSTANDING").order_by(
            "-checkout_date"
        )
        return queryset


class ReturnItemView(LibrarianViewBase, ListView):
    template_name = "management/return_item.html"
    model = Checkout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active = self.request.GET.get("active")
        context["form"] = ReturnCheckoutForm()
        if self.get_queryset().filter(pk=active).exists():
            context["active"] = self.get_queryset().get(pk=active)
        return context

    def get_queryset(self):
        queryset = super(ReturnItemView, self).get_queryset()
        queryset = queryset.filter(checkout_status="OUTSTANDING").order_by(
            "-checkout_date"
        )
        return queryset

    def post(self, request, *args, **kwargs):
        checkout = get_object_or_404(Checkout, pk=request.POST.get("checkout_id"))
        form = ReturnCheckoutForm(request.POST)
        is_valid = form.is_valid()
        if not is_valid:
            # render w/ errors
            return render(
                request,
                self.template_name,
                {
                    "active": checkout,
                    "form": form,
                    "object_list": self.get_queryset,
                },
            )
        else:
            checkout_id = form.cleaned_data["checkout_id"]
            condition = form.cleaned_data["return_condition"]
            checkout = Checkout.objects.get(pk=checkout_id)
            checkout_manager.return_items(checkout, condition)
            return redirect("librarian-control-panel")


class AddItemView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "/login/"
    redirect_field_name = None
    raise_exception = True
    template_name = "management/add_item.html"

    def test_func(self):
        """
        Test the user is part of the librarian group
        """
        return librarian_check(self.request.user)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = AddItemForm(request.POST)
        if form.is_valid():
            # Retrieve clean data from form
            data = form.cleaned_data
            cleaner = Cleaner()

            # Send data to the manager
            item = inventory_manager.create_itemgroup_record(
                make=data.get("make"),
                model=data.get("model"),
                # Wrap the description in a div to ensure the document has a root node
                description=cleaner.clean_html(f"<div>{data.get('description')}</div>"),
                moniker=data.get("moniker"),
                default_checkout_len=data.get("default_checkout_len"),
            )
            messages.success(request, f"{item} successfully added to catalogue.")
            return redirect("librarian-control-panel")
        else:
            return render(request, self.template_name, {"form": form})


class AddHoldingView(LibrarianViewBase, ListView):
    template_name = "management/add_holding.html"
    queryset = ItemGroup.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active = self.request.GET.get("active")
        context["form"] = AddHoldingForm()
        if self.get_queryset().filter(pk=active).exists():
            context["active"] = self.queryset.get(pk=active)
        return context

    def post(self, request):
        form = AddHoldingForm(request.POST)
        if form.is_valid():
            # Retrieve clean data from form
            data = form.cleaned_data

            # Send data to the manager
            item = inventory_manager.create_item_record(
                itemgroup_id=data["itemgroup_id"],
                library_id=data["library_id"],
                serial_num=data["serial_num"],
                condition=data["condition"],
                availability=data["availability"],
                notes=data["notes"],
                date_acquired=data.get("date_acquuired", timezone.now()),
                last_inspected=data.get("last_inspected", timezone.now()),
            )
            messages.success(request, f"{item} successfully added to inventory.")
            return redirect("librarian-control-panel")
        else:
            try:
                active = self.queryset.get(pk=self.request.POST.get("itemgroup_id"))
            except ItemGroup.DoesNotExist:
                active = None
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "active": active,
                    "object_list": self.queryset,
                },
            )


class MasterInventoryView(LibrarianViewBase, ListView):
    queryset = ItemGroup.objects.all()
    template_name = "management/master_inventory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        about_views = ["features", "links"]

        # The id of our selected item
        active = self.request.GET.get("active")
        about_view = self.request.GET.get("about_view")
        if about_view not in about_views:
            about_view = None
        # Set the context variable if the item exists in our dataset
        if self.get_queryset().filter(pk=active).exists():
            context["active"] = self.queryset.get(pk=active)
            context["active_item_set"] = context["active"].item_set.all()
            context["about_view"] = about_view
        return context


class UpdateItemView(LibrarianViewBase, SingleObjectMixin, TemplateView):
    template_name = "management/update_item.html"
    model = Item

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["form"] = UpdateItemForm()
        return context

    def post(self, request, pk):
        form = UpdateItemForm(request.POST)
        valid = form.is_valid()

        if valid:
            item = self.get_object()
            item.availability = form.cleaned_data.get("availability")
            item.condition = form.cleaned_data.get("condition")
            item.notes = form.cleaned_data.get("notes")
            try:
                item.full_clean()
                item.save()
                return redirect(
                    f"{reverse('master-inventory')}?active={item.item_group_id}"
                )
            except ValidationError:
                # TODO: return form w/ additional errors?
                return HttpResponseBadRequest()
        else:
            # Pop an error message, maybe?
            return render(request, self.template_name, {"form": form})


class DeleteItemView(LibrarianViewBase, SingleObjectMixin, TemplateView):
    template_name = "management/delete_item.html"
    model = Item

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["form"] = DeleteItemForm()
        return context

    def post(self, request, *args, **kwargs):
        form = DeleteItemForm(request.POST)
        form.full_clean()
        valid = form.is_valid()
        self.object = self.get_object()

        if valid:
            itemgroup_id = self.object.item_group_id
            # Delete all related checkout entries
            Checkout.objects.filter(item=self.object).delete()
            # Then delete the item
            self.object.delete()
            return redirect(f"{reverse('master-inventory')}?active={itemgroup_id}")
        else:
            return render(
                request, self.template_name, {"form": form, "object": self.object}
            )
