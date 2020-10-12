from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View
from django.views.decorators.http import require_http_methods

from bibliotech.forms import LoginForm, SignupForm


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        form.is_valid()

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Nav to success page
            return redirect(request.POST.get("next", "itemgroup-list"))
        else:
            # Return to login page
            # TODO: Display some errors
            return render(request, "bibliotech/login.html")
    # Redirect to home if the user is logged in already
    elif request.user.is_authenticated:
        return redirect("itemgroup-list")
    else:
        # I don't think this actually does anything anymore...
        form = LoginForm()
        return render(request, "bibliotech/login.html", {"form": form})


@require_http_methods(["POST"])
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    # Redirect to value specified by 'return' otherwise, redirect to th list view
    return redirect(request.POST.get("next", "home"))


class SignUpView(View):
    template_name = "bibliotech/signup.html"

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return render(
                request,
                self.template_name,
            )

    def post(self, request, **kwargs):
        form = SignupForm(request.POST)
        form.full_clean()
        valid = form.is_valid()
        if valid:
            data = form.cleaned_data
            try:
                user = User.objects.create_user(
                    username=data.get("username"), email=data.get("email")
                )
                user.set_password(data.get("password"))
                user.first_name = data.get("fname")
                user.last_name = data.get("lname")
                user.save()
                login(request, user)
                return redirect(reverse("home"))
            except Exception as e:
                print(e)
        else:
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                },
            )
