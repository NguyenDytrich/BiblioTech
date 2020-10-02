from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View

from bibliotech.models import Checkout, Item, ItemGroup

import bibliotech.checkout_manager as checkout_manager


def has_librarian_permissions(user):
    """
    Test that the user has permission to act as a librarian.
    """
    groups = user.groups.all()
    # TODO: Don't do this.
    return True


class LibrarianView(View):
    template_name = "bibliotech/librarian_control_panel.html"

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
