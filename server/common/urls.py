from django.urls import path

from . import views

app_name = "common"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("guest_home", views.GuestHomeView.as_view(), name="guest_home"),
]
