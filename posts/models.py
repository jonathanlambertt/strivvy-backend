import uuid

from django.db import models
from users.models import User

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    main_image = models.URLField()
    favicon = models.URLField()
    site_name = models.CharField(max_length=255)
    url = models.URLField()

