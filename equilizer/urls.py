***REMOVED***equilizer URL Configuration

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
***REMOVED***
from django.contrib import admin
from django.urls import path

from equilizer.views import (
    ItemGroupListView,
    ItemGroupDetailView,
    CheckoutListView,
    home_view,
    login_view,
    logout_view,
    add_to_cart,
    cart_view,
    create_checkout,
    success
)

from equilizer.class_views.admin_views import LibrarianView

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
    path("", home_view, name="home")
***REMOVED***
