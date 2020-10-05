from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError, PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView
from django.urls import reverse

from bibliotech.forms import DenyCheckoutForm
from bibliotech.models import Checkout, Item
import bibliotech.checkout_manager as checkout_manager


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


class LibrarianView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "bibliotech/librarian_control_panel.html"
    raise_exception = True

    def test_func(self):
        """
        Test the user is part of the librarian group
        """
        return librarian_check(self.request.user)

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


class DenyCheckoutView(LoginRequiredMixin, UserPassesTestMixin, View):
    raise_exception = True

    def test_func(self):
        """
        Test the user is part of the librarian group
        """
        return librarian_check(self.request.user)

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
                "bibliotech/deny_checkout.html",
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
                "bibliotech/deny_checkout.html",
                {"checkout_id": checkout_id, "form": form},
            )

        else:
            # TODO: implement an audit log of denied checkouts
            reason = form.cleaned_data.get("reason")
            checkout_manager.deny_checkout(checkout)
            return redirect(reverse("librarian-control-panel"))


class MasterCheckoutListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = "/login/"
    redirect_field_name = None
    raise_exception = True
    model = Checkout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def test_func(self):
        return librarian_check(self.request.user)

    # TODO: Test this
    def get_queryset(self):
        queryset = super(MasterCheckoutListView, self).get_queryset()
        queryset = queryset.filter(checkout_status="OUTSTANDING").order_by(
            "-checkout_date"
        )
        return queryset


class ReturnItemView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "bibliotech/return_item.html"
    login_url = "/login/"
    redirect_field_name = None
    raise_exception = True
    model = Checkout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active = self.request.GET.get("active")
        context["return_condition_choices"] = [x[0] for x in Item.Condition.choices]
        if self.get_queryset().filter(pk=active).exists():
            context["active"] = self.get_queryset().get(pk=active)
        return context

    def test_func(self):
        """
        Test the user is part of the librarian group
        """
        return librarian_check(self.request.user)

    def get_queryset(self):
        queryset = super(ReturnItemView, self).get_queryset()
        queryset = queryset.filter(checkout_status="OUTSTANDING").order_by(
            "-checkout_date"
        )
        return queryset

    def post(self, request, *args, **kwargs):
        get_object_or_404(Checkout, pk=request.POST.get("checkout_id"))
        form = ReturnCheckoutForm(request.POST)
        is_valid = form.is_valid()
        if not is_valid:
            # TODO: redirect w/ errors
            return redirect(
                f'{reverse("return-item")}?active={request.POST["checkout_id"]}',
            )
        else:
            checkout_id = form.cleaned_data["checkout_id"]
            condition = form.cleaned_data["return_condition"]
            checkout = Checkout.objects.get(pk=checkout_id)
            checkout_manager.return_items(checkout, condition)
            return redirect("librarian-control-panel")
