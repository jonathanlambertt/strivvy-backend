import uuid
from django.db import models

from users.models import User
from posts.models import Post

class Like(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
