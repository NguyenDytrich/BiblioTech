"""bibliotech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from bibliotech.views.login import login_view, logout_view
from bibliotech.views.catalogue import ItemGroupListView, ItemGroupDetailView
from bibliotech.views.cart import cart_view, add_to_cart
from bibliotech.views.checkout import CheckoutListView, create_checkout
from bibliotech.views.librarian import (
    approve_checkout,
    LibrarianView,
    DenyCheckoutView,
    ReturnItemView,
    MasterCheckoutListView,
    AddItemView,
    AddHoldingView,
    MasterInventoryView,
)
from bibliotech.views.misc import home_view, success

urlpatterns = [
    path("admin/", admin.site.urls),
    path("control_panel/", LibrarianView.as_view(), name="librarian-control-panel"),
    path("items", ItemGroupListView.as_view(), name="itemgroup-list"),
    path("items/<int:pk>/", ItemGroupDetailView.as_view(), name="itemgroup-detail"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("cart/", cart_view, name="cart-view"),
    path("cart/add/<int:itemgroup_id>", add_to_cart, name="cart-add"),
    path("checkout/", create_checkout, name="create-checkout"),
    path("success/", success, name="success-view"),
    path("checkouts/", CheckoutListView.as_view(), name="checkout-list"),
    path(
        "checkouts/<int:checkout_id>/approve", approve_checkout, name="approve-checkout"
    ),
    path(
        "checkouts/<int:checkout_id>/deny",
        DenyCheckoutView.as_view(),
        name="deny-checkout",
    ),
    path("control_panel/returns", ReturnItemView.as_view(), name="return-item"),
    path(
        "control_panel/checkouts",
        MasterCheckoutListView.as_view(),
        name="all-checkouts",
    ),
    path("control_panel/add_item", AddItemView.as_view(), name="add-item"),
    path("control_panel/add_holding", AddHoldingView.as_view(), name="add-holding"),
    path(
        "control_panel/master_inventory",
        MasterInventoryView.as_view(),
        name="master-inventory",
    ),
    path("", home_view, name="home"),
]
