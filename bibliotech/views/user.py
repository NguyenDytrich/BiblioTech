from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

from bibliotech.forms import UpdatePasswordForm, UpdateProfileForm
from library.models import Member


class UserMember:
    """
    DTO object that gets the User and its related Member model.
    """

    def __init__(self, id):
        self.user = get_object_or_404(User, pk=id)
        self.member = get_object_or_404(Member, user=self.user)

    def __str__(self):
        return f"{self.member.member_id} ({self.user.get_full_name()}"


class UserProfileView(LoginRequiredMixin, View):
    template_name = "bibliotech/user_profile.html"
    login_url = "/login/"

    def get_user_member(self, pk):
        return UserMember(pk)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden
        profile = self.get_user_member(request.user.id)
        return render(request, self.template_name, {"profile": profile})


class UserProfileUpdateView(LoginRequiredMixin, View):
    template_name = "bibliotech/update_profile.html"

    def get(self, request, *args, **kwargs):
        """
        Renders the profile update form
        """
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """
        Update the user's profile information based on the request body
        """
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get("fname")
            user.last_name = form.cleaned_data.get("lname")
            user.email = form.cleaned_data.get("email")
            user.save()
            return redirect("user-profile")
        else:
            return render(request, self.template_name, {"form": form})


class UserPasswordUpdateView(LoginRequiredMixin, View):
    template_name = "bibliotech/update_password.html"

    def get(self, request, *args, **kwargs):
        """
        Renders the update password form
        """
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """
        Updates the user's password if all fields are valid, and the
        user id matches the user id of the authenticated user
        """
        user = User.objects.get(pk=request.user.id)
        form = UpdatePasswordForm(request.POST)
        valid = False

        # Cleaning the UpdatePasswordForm will raise DoesNotExist
        # if a user does not exist specified  by the user_id
        try:
            valid = form.is_valid()
        except User.DoesNotExist:
            return HttpResponseForbidden()

        if form.is_valid():
            if user.id != form.cleaned_data.get("user_id"):
                return HttpResponseForbidden()
            else:
                user.set_password(form.cleaned_data.get("new_password"))
                user.save()
                update_session_auth_hash(request, user)
                return redirect("user-profile")
        else:
            return render(request, self.template_name, {"form": form})
