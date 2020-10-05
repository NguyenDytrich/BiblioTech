from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from bibliotech.forms import LoginForm

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
