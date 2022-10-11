from django.urls import path

from . import views

app_name = "matchs"

urlpatterns = [
    path("create/", views.MatchCreateView.as_view(), name="match_create"),
    path("<uuid:match_id>", views.MatchView.as_view(), name="match"),
    path("<uuid:match_id>/start", views.MatchStartView.as_view(), name="match_start"),
]
