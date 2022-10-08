from django import forms
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

# from .forms import MatchForm
from .models import Match, Member
from .logics import LogicService


class MatchView(TemplateView):
    template_name = "matchs/match.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["match_name"] = Match.objects.get(pk=self.kwargs["match_id"]).match_name
        ctx["id"] = Match.objects.get(pk=self.kwargs["match_id"]).id
        ctx["number_of_member"] = Member.objects.filter(
            match=self.kwargs["match_id"]
        ).count()
        ctx["member_names"] = Member.objects.filter(
            match=self.kwargs["match_id"]
        ).values_list("member_name", flat=True)
        return ctx

    def post(self, request, *args, **kwargs):
        match = get_object_or_404(Match, id=self.kwargs["match_id"])
        members_list = Member.objects.filter(match=self.kwargs["match_id"]).values_list(
            "member_name", flat=True
        )
        logic = LogicService(match.number_of_court, len(members_list))
        match.match_list = logic.start_game()
        print(111)
        return redirect("matchs:match_start", match_id=match.id)


class MatchCreateView(View):
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            member_names = request.POST.getlist("member_name")
            owner = request.user
            match_name = request.POST.get("match_name")
            number_of_court = request.POST.get("number_of_court")
            match = Match.objects.create(
                owner=owner, match_name=match_name, number_of_court=number_of_court
            )
            member_instance = [
                Member(member_name=name, match=match) for name in member_names
            ]
            Member.objects.bulk_create(member_instance)
        return redirect("matchs:match_create", match_id=match.id)

    def get(self, request, *args, **kwargs):
        return render(request, "matchs/match_create.html")


class MatchStartView(View):
    template_name = "matchs/match_start.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        match = get_object_or_404(Match, id=self.kwargs["match_id"])
        members_list = Member.objects.filter(match=self.kwargs["match_id"]).values_list(
            "member_name", flat=True
        )
        extend = {
            "match": match,
            "members_list": members_list,
            "start_match_list": match.match_list,
            "id": self.kwargs["match_id"],
        }
        ctx.update(extend)
        return ctx

    def get(self, request, *args, **kwargs):
        return redirect("matchs:match_start", match_id=self.kwargs["match_id"])

    def post(self, request, *args, **kwargs):
        match = get_object_or_404(Match, id=self.kwargs["match_id"])
        print(match)
        members_list = Member.objects.filter(match=self.kwargs["match_id"]).values_list(
            "member_name", flat=True
        )
        context = {
            "match": match,
            "members_list": members_list,
            "start_match_list": match.match_list,
            "id": self.kwargs["match_id"],
        }
        return render(request, "matchs/match_start.html", context)
