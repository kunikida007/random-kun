import random

from .models import Match, Member


class LogicService:
    def __init__(self, match=None, court=None):
        self._match = match
        self._court = court

    def generate_match_list(self):
        match_member = [[], []]
        for i in range(2):
            for _ in range(2):
                member = (
                    Member.objects.filter(match=self._match, court_number=0)
                    .order_by("?")
                    .first()
                )
                member.court_number = self._court
                member.save()
                match_member[i].append(member.member_name)
        self._match.match_list[self._court - 1] = match_member
        self._match.save()

    def chose_random_member_first(self, number_of_court):
        match_member = [[], []]
        for i in range(2):
            for _ in range(2):
                member = (
                    Member.objects.filter(match=self._match, court_number=0)
                    .order_by("?")
                    .first()
                )
                member.court_number = number_of_court
                member.save()
                match_member[i].append(member.member_name)
        self._match.match_list.append(match_member)
        self._match.save()

    def start_game(self):
        self._match.match_list = []
        self._match.save()
        Member.objects.filter(match=self._match).update(court_number=0)
        for i in range(self._match.number_of_court):
            self.chose_random_member_first(i + 1)

    def random_game(self):
        self._match.match_list = []
        self._match.save()
        Member.objects.filter(match=self._match).update(court_number=0)
        for i in range(self._match.number_of_court):
            self.chose_random_member_first(i + 1)

    def restore_members_status(self):
        Member.objects.filter(match=self._match, court_number=self._court).update(
            court_number=0
        )

    def next_game(self, court_number, red, blue):
        self.update_score(court_number, red, blue)
        self.restore_members_status()
        self.generate_match_list()

    def generate_goals_score(self, red, blue):
        red_goals_score = red - blue
        blue_goals_score = blue - red
        return red_goals_score, blue_goals_score

    def update_score(self, court_number, red, blue):
        red_goals_score, blue_goals_score = self.generate_goals_score(red, blue)
        red_member = self._match.match_list[court_number - 1][0]
        blue_member = self._match.match_list[court_number - 1][1]
        for name in red_member:
            member = Member.objects.get(member_name=name, match=self._match)
            member.goals_score = red_goals_score
            member.match_count += 1
            member.save()
        for name in blue_member:
            member = Member.objects.get(member_name=name, match=self._match)
            member.goals_score = blue_goals_score
            member.match_count += 1
            member.save()
    
    def get_rank(self, members):
        for member in members:
            try:
                goals_score_rate = member.goals_score / member.match_count
            except ZeroDivisionError:
                goals_score_rate = 0
            member.goals_score_rate = goals_score_rate
            member.save()
