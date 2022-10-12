import random

from .models import Match, Member


class LogicService:
    def __init__(self, match, court=None):
        self._match = match
        self._court = court

    def chose_random_member(self):
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
        Member.objects.filter(match=self._match).update(court_number=0)
        for i in range(self._match.number_of_court):
            self.chose_random_member_first(i + 1)

    def restore_members_status(self):
        Member.objects.filter(match=self._match, court_number=self._court).update(
            court_number=0
        )

    def next_game(self):
        self.restore_members_status()
        self.chose_random_member()
