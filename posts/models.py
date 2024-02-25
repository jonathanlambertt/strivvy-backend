import uuid
from django.utils import timezone
from django.db import models
from users.models import User

def get_current_time():
    return timezone.now()

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    date = models.DateTimeField(default=get_current_time)
    description = models.CharField(max_length=255, blank=True, null=True, default="null")
    title = models.CharField(max_length=255, blank=True, null=True, default="null")
    thumbnail = models.URLField(max_length=500, blank=True, null=True, default="null")
    favicon = models.URLField(blank=True, null=True, default="null")
    site_name = models.CharField(max_length=255, blank=True, null=True, default="null")

