from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render

from .models import Match, Member
from .logics import LogicService


class MatchView(TemplateView):
    template_name = "matchs/match.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        match = get_object_or_404(Match, pk=self.kwargs["match_id"])
        ctx["match_name"] = match.match_name
        ctx["id"] = match.id
        ctx["number_of_member"] = Member.objects.filter(
            match=self.kwargs["match_id"]
        ).count()
        ctx["member_names"] = Member.objects.filter(
            match=self.kwargs["match_id"]
        ).values_list("member_name", flat=True)
        return ctx

    def post(self, request, *args, **kwargs):
        if "btn_start" in request.POST:
            match = get_object_or_404(Match, id=self.kwargs["match_id"])
            LogicService(match=match).start_game()
            return redirect("matchs:match_start", match.id)


class MatchCreateView(View):
    def post(self, request, *args, **kwargs):
        members_list = request.POST.getlist("member_name")
        owner = request.user
        match_name = request.POST.get("match_name")
        number_of_court = request.POST.get("number_of_court")
        match = Match.objects.create(
            owner=owner,
            match_name=match_name,
            number_of_court=number_of_court,
        )
        member_instance = [
            Member(member_name=name, match=match) for name in members_list
        ]
        Member.objects.bulk_create(member_instance)
        return redirect("matchs:match", match.id)

    def get(self, request, *args, **kwargs):
        return render(request, "matchs/match_create.html")


class MatchStartView(TemplateView):
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

    def post(self, request, *args, **kwargs):
        match = get_object_or_404(Match, id=self.kwargs["match_id"])
        members_list = Member.objects.filter(
                    match=self.kwargs["match_id"]
                ).values_list("member_name", flat=True)
        context = {
                    "match": match,
                    "members_list": members_list,
                    "match_list": match.match_list,
                    "id": self.kwargs["match_id"],
                }
        if f"btn_shuffle" in request.POST:
            LogicService(match=match).start()
        for i in range(match.number_of_court):
            if f"btn_game{i+1}_end" in request.POST:
                LogicService(match, i+1).next_game()
        # if "btn_end" in request.POST:    
        return render(request, "matchs/match_start.html", context=context)
