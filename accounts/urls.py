from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.profile_edit_view, name='profile_edit'),
    path('user/<str:username>/', views.profile_view, name='profile'),
    path('user/<str:username>/follow/', views.follow_toggle_view, name='follow_toggle'),
    path('user/<str:username>/followers/', views.followers_list_view, name='followers_list'),
    path('user/<str:username>/following/', views.following_list_view, name='following_list'),
]
