from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # path('login/',views.login, name ='login'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    
]
