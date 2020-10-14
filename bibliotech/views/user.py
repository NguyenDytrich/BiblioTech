from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views import View

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
    redirect_field_name = None

    def get_user_member(self, pk):
        return UserMember(pk)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden
        profile = self.get_user_member(request.user.id)
        return render(request, self.template_name, {"profile": profile})
