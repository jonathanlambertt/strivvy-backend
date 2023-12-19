from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.create_user)
]