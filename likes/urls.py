from django.urls import path
from . import views

app_name = 'likes'
urlpatterns = [
    path('<uuid:post_id>', views.create_like),
    path('delete/<uuid:like_id>', views.delete_like)
]