from rest_framework.authtoken import views as drf_views
from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.create_user),
    path('follow/<uuid:user_id>', views.follow_user),
    path('unfollow/<uuid:user_id>', views.unfollow_user),
    path('login', drf_views.obtain_auth_token),
    path('search/', views.search_for_user),
    path('profile', views.get_profile),
    path('feed', views.get_feed)
]