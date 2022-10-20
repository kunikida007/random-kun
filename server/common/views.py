from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "common/home.html"

    def post(self, request, *args, **kwargs):
        if "btn_start" in request.POST:
            return redirect("matchs:match_create")
        elif "btn_login" in request.POST:
            return redirect("users:login")
        elif "btn_signup" in request.POST:
            return redirect("users:signup")
        elif "btn_continue" in request.POST:
            return redirect("matchs:match_continue")
        elif "btn_logout" in request.POST:
            return redirect("users:logout")
        return render(request, "common/home.html")
