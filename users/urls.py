from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.create_user),
    path('follow/<uuid:user_id>', views.follow_user)
]