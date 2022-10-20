from django.contrib import admin

from .models import Match, Member


class MatchAdmin(admin.ModelAdmin):
    fields = ["owner", "match_name", "number_of_court", "match_list"]


class MemberAdmin(admin.ModelAdmin):
    fields = ["member_name", "match", "court_number", "goals_score", "match_count"]


admin.site.register(Match, MatchAdmin)
admin.site.register(Member, MemberAdmin)
