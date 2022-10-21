import random

from .models import Match, Member


class MemberService:
    @classmethod
    def count_members(cls, match):
        return Member.objects.filter(match=match).count()

    @classmethod
    def get_filtered_member_names(cls, match):
        return Member.objects.filter(match=match).values_list("member_name", flat=True)

    @classmethod
    def create_match(cls, owner, match_name, number_of_court, type):
        if owner.is_anonymous:
            match = Match.objects.create(
                match_name=match_name, number_of_court=number_of_court, type=type
            )
        else:
            match = Match.objects.create(
                owner=owner,
                match_name=match_name,
                number_of_court=number_of_court,
                type=type
            )
        return match

    @classmethod
    def create_members(cls, match, members_list):
        member_instance = [
            Member(member_name=name, match=match, court_number=0)
            for name in members_list
        ]
        Member.objects.bulk_create(member_instance)

    # Noneを無くす
    @classmethod
    def get_members_list(cls, member_names):
        members_list = [name for name in member_names if name != None]
        return members_list

    @classmethod
    def update_match(cls, match, match_name, number_of_court):
        match.match_name = match_name
        match.number_of_court = number_of_court
        match.save()
        # 古いメンバーは消す
        Member.objects.filter(match=match).delete()
    
    @classmethod
    def start_game_same(cls, match):
        
