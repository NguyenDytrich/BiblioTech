from django.core.exceptions import ValidationError, PermissionDenied
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from bibliotech.models import Checkout
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
