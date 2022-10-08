from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # path('login/',views.login, name ='login'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    # path('<int:user_id>/follow_list/', views.follow_list, name='follow_list'),
    # path('<int:user_id>/follower_list/', views.follower_list, name='follower_list'),
    # path('<int:user_id>/follow/', views.follow, name='follow'),
    # path('<int:user_id>/unfollow/', views.unfollow, name='unfollow'),
    # path('logout/', views.LogoutView.as_view(), name="logout"),
    
]
