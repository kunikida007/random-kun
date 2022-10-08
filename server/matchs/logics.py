import random

from .models import Match

members_status = {}


class LogicService:
    def __init__(self, court, member):
        global members_status
        self.court = court
        self.member = member
        self._members_status = members_status
        self._match_list = []

    def _generate_members_status(self):
        self._members_status = {i + 1: 0 for i in range(self.member)}

    def _generate_match_list(self):
        self._match_list = [[] for _ in range(self.court)]

    def chose_random_not_same_time(self, number_of_court):
        match = [[], []]
        for i in range(2):
            while len(match[i]) < 2:
                member = random.choice(list(self._members_status.keys()))
                if self._members_status[member] == 0:
                    match[i].append(member)
                self._members_status[member] = number_of_court
        return match

    def start_game(self):
        self._generate_members_status()
        self._generate_match_list()
        for i in range(self.court):
            self._match_list[i] = self.chose_random_not_same_time(i + 1)
        return self._match_list

    def restore_members_status(self, number_of_court):
        restore_members = [
            m for m, v in self._members_status().items if v == number_of_court
        ]
        if not restore_members:
            for member in restore_members:
                self._members_status[member] = 0

    def finish_game(self, number_of_court):
        self.restore_members_status(number_of_court)
        self._match_list[number_of_court - 1] = self.chose_random_not_same_time(
            number_of_court
        )
