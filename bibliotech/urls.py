from django.contrib import admin
from django.urls import include, path

from bibliotech.views.login import login_view, logout_view, SignUpView

urlpatterns = [
    path("", include('library.urls')),
    path("management/", include('management.urls')),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("admin/", admin.site.urls),
]
