from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password_reset_form/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            from_email=" maroonv4869@gmail.com ",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_mail_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset/<str:uidb64>/<str:token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirmation.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_finish/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_finish.html"
        ),
        name="password_reset_complete",
    ),
]
