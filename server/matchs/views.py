from django.contrib.auth.mixins import LoginRequiredMixin
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
        match = get_object_or_404(Match, id=self.kwargs["match_id"])
        if "btn_start" in request.POST:
            LogicService(match=match).start_game()
            return redirect("matchs:match_start", match.id)
        if "btn_update" in request.POST:
            return redirect("matchs:match_update", match.id)


class MatchCreateView(View):
    def post(self, request, *args, **kwargs):
        members_list = [
            name for name in request.POST.getlist("member_name") if name != None
        ]
        owner = request.user
        match_name = request.POST.get("match_name")
        number_of_court = request.POST.get("number_of_court")
        if not owner.is_anonymous:
            match = Match.objects.create(
                owner=owner,
                match_name=match_name,
                number_of_court=number_of_court,
            )
        else:
            match = Match.objects.create(
                match_name=match_name,
                number_of_court=number_of_court,
            )
        member_instance = [
            Member(member_name=name, match=match, court_number=0)
            for name in members_list
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
        extend = {
            "match": match,
            "id": self.kwargs["match_id"],
        }
        print(match.match_list)
        ctx.update(extend)
        print(ctx)
        return ctx

    def post(self, request, *args, **kwargs):
        match = get_object_or_404(Match, id=self.kwargs["match_id"])
        if "btn_random" in request.POST:
            LogicService(match=match).random_game()
        for i in range(match.number_of_court):
            if f"btn_game{i+1}_end" in request.POST:
                LogicService(match, i + 1).next_game()
        if "btn_end" in request.POST:
            return redirect("common:home")
        if "btn_update" in request.POST:
            return redirect("matchs:match_update", match.id)
        return redirect("matchs:match_start", match.id)


class MatchContinueView(TemplateView, LoginRequiredMixin):
    template_name = "matchs/match_continue.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        matches = Match.objects.filter(owner=self.request.user)
        extend = {
            "matchs": matches,
        }
        ctx.update(extend)
        return ctx

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if "match" in request.POST:
            match_id = request.POST.get("match")
            return redirect("matchs:match", match_id)


class MatchUpdateView(TemplateView):
    template_name = "matchs/match_update.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        match = get_object_or_404(Match, pk=self.kwargs["match_id"])
        members = Member.objects.filter(match=match).values_list(
            "member_name", flat=True
        )
        extend = {"match": match, "members": members}
        ctx.update(extend)
        return ctx

    def post(self, request, *args, **kwargs):
        if "btn_start" in request.POST:
            members_list = [
                name for name in request.POST.getlist("member_name") if name != None
            ]
            match_name = request.POST.get("match_name")
            number_of_court = request.POST.get("number_of_court")
            match = get_object_or_404(Match, pk=self.kwargs["match_id"])
            match.match_name = match_name
            match.number_of_court = number_of_court
            match.save()
            print(Member.objects.filter(match=match))
            Member.objects.filter(match=match).delete()
            member_instance = [
                Member(member_name=name, match=match) for name in members_list
            ]
            Member.objects.bulk_create(member_instance)
            return redirect("matchs:match", match.id)
