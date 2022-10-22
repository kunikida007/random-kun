from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "common/home.html"

    def post(self, request, *args, **kwargs):
        if "btn_start" in request.POST:
            return redirect("matchs:match_create")
        elif "btn_continue" in request.POST:
            return redirect("matchs:match_continue")
        return redirect("common:home")


class GuestHomeView(TemplateView):
    template_name = "common/guest_home.html"

    def post(self, request, *args, **kwargs):
        if "btn_start" in request.POST:
            return redirect("matchs:match_create")
        return redirect("common:guest_home")
