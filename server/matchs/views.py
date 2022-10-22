from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .models import Match, Member
from .logics import LogicService
from .services import MemberService


class MatchView(TemplateView):
    template_name = "matchs/match.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        match = get_object_or_404(Match, pk=self.kwargs["match_id"])
        ctx["match"] = match
        ctx["number_of_member"] = MemberService.count_members(match)
        ctx["member_names"] = MemberService.get_filtered_member_names(match)
        return ctx

    def post(self, request, *args, **kwargs):
        match = get_object_or_404(Match, id=self.kwargs["match_id"])
        if "btn_start" in request.POST:
            LogicService(match=match).start_game()
            return redirect("matchs:match_start", match.id)
        if "btn_end" in request.POST:
            if request.user.is_authenticated:
                return redirect("common:home")
            else:
                return redirect("common:guest_home")


class MatchCreateView(TemplateView):
    template_name = "matchs/match_create.html"

    def post(self, request, *args, **kwargs):
        members_list = MemberService.get_members_list(
            request.POST.getlist("member_name")
        )
        owner = request.user
        match_name = request.POST.get("match_name")
        number_of_court = request.POST.get("number_of_court")
        type = request.POST.get("match_type")
        if "btn_start" in request.POST:
            if (int(number_of_court) * 4) > len(members_list):
                request.session["data"] = request.POST
                request.session["members_list"] = members_list
                messages.error(request, "1コートの人数が4人以下になります。")
                return redirect("matchs:match_create")
            match = MemberService.create_match(owner, match_name, number_of_court, type)
            MemberService.create_members(match, members_list)
            return redirect("matchs:match", match.id)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # 入力が中断された場合のセッションの保存
        if self.request.session.get("data"):
            extend = {
                "members": self.request.session.get("members_list"),
                "match_name": self.request.session.get("data").get("match_name"),
                "number_of_court": self.request.session.get("data").get(
                    "number_of_court"
                ),
            }
            ctx.update(extend)
        return ctx


class MatchStartView(TemplateView):
    template_name = "matchs/match_start.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        match = get_object_or_404(Match, id=self.kwargs["match_id"])
        extend = {
            "match": match,
        }
        ctx.update(extend)
        return ctx

    def post(self, request, *args, **kwargs):
        match = get_object_or_404(Match, id=self.kwargs["match_id"])
        if "btn_random" in request.POST:
            LogicService(match=match).random_game()
        for i in range(match.number_of_court):
            print(i, request.POST)
            if f"btn_game{i+1}_end" in request.POST or "btn_match_end" in request.POST:
                red = request.POST.get(f"redscore{i+1}")
                blue = request.POST.get(f"bluescore{i+1}")
                if not red or not blue:
                    messages.error(request, "スコアを入力してください")
                    return redirect("matchs:match_start", match.id)
                LogicService(match, i + 1).next_game(
                    court_number=i + 1, red=int(red), blue=int(blue)
                )
        if "btn_results" in request.POST:
            print(1)
            return redirect("matchs:match_results", match.id)
        if "btn_end" in request.POST:
            return redirect("matchs:match_final_results", match.id)
        if "btn_update" in request.POST:
            return redirect("matchs:match_update", match.id)
        return redirect("matchs:match_start", match.id)


class MatchContinueView(TemplateView, LoginRequiredMixin):
    template_name = "matchs/match_continue.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        matches = Match.objects.filter(owner=self.request.user, is_active=True)
        extend = {
            "matchs": matches,
        }
        ctx.update(extend)
        return ctx

    def post(self, request, *args, **kwargs):
        if "match" in request.POST:
            print(request.POST)
            match_id = request.POST.get("match")
            return redirect("matchs:match", match_id)


class MatchUpdateView(TemplateView):
    template_name = "matchs/match_update.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        match = get_object_or_404(Match, pk=self.kwargs["match_id"])
        members = MemberService.get_filtered_member_names(match)
        extend = {"match": match, "members": members}
        ctx.update(extend)
        return ctx

    def post(self, request, *args, **kwargs):
        if "btn_start" in request.POST:
            MemberService.get_members_list(request.POST.getlist("member_name"))
            match = get_object_or_404(Match, pk=self.kwargs["match_id"])
            MemberService.update_match(
                match,
                request.POST.get("match_name"),
                request.POST.get("number_of_court"),
            )
            MemberService.count_members(match)
            return redirect("matchs:match", match.id)


class MatchResultsView(TemplateView):
    template_name = "matchs/match_results.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        match = get_object_or_404(Match, pk=self.kwargs["match_id"])
        members = Member.objects.filter(match=match)
        LogicService().get_rank(members)
        members = Member.objects.filter(match=match).order_by("-goals_score_rate")
        extend = {"match": match, "members": members}
        ctx.update(extend)
        return ctx


class MatchFinalResultsView(TemplateView):
    template_name = "matchs/match_final_results.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        match = get_object_or_404(Match, pk=self.kwargs["match_id"])
        members = Member.objects.filter(match=match)
        LogicService().get_rank(members)
        members = Member.objects.filter(match=match).order_by("-goals_score_rate")
        extend = {"match": match, "members": members}
        ctx.update(extend)
        return ctx

    def post(self, request, *args, **kwargs):
        if "btn_end" in request.POST:
            if request.user.is_authenticated:
                return redirect("common:home")
            else:
                return redirect("common:guest_home")
        return redirect("matchs:match_final_results", self.kwargs["match.id"])
