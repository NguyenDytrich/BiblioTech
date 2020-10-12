from django.urls import path

from management.views.librarian import (
    approve_checkout,
    LibrarianView,
    DenyCheckoutView,
    ReturnItemView,
    MasterCheckoutListView,
    AddItemView,
    AddHoldingView,
    MasterInventoryView,
    UpdateItemView,
    UpdateItemGroupView,
    DeleteItemView,
)

urlpatterns = [
    path(
        "checkouts/<int:checkout_id>/deny",
        DenyCheckoutView.as_view(),
        name="deny-checkout",
    ),
    path(
        "checkouts/<int:checkout_id>/approve", approve_checkout, name="approve-checkout"
    ),
    path("", LibrarianView.as_view(), name="librarian-control-panel"),
    path("returns", ReturnItemView.as_view(), name="return-item"),
    path(
        "checkouts",
        MasterCheckoutListView.as_view(),
        name="all-checkouts",
    ),
    path("inventory/add/item", AddItemView.as_view(), name="add-item"),
    path("inventory/add/holding", AddHoldingView.as_view(), name="add-holding"),
    path(
        "inventory",
        MasterInventoryView.as_view(),
        name="master-inventory",
    ),
    path(
        "inventory/<int:pk>/update",
        UpdateItemView.as_view(),
        name="update-item",
    ),
    path(
        "inventory/<int:pk>/delete",
        DeleteItemView.as_view(),
        name="delete-item",
    ),
    path(
        "items/<int:pk>/update",
        UpdateItemGroupView.as_view(),
        name="update-itemgroup",
    ),
]
