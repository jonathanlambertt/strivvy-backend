import uuid
import redis

from django.contrib.auth.models import AbstractUser
from django.db import models

redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def distribute_post_to_followers(self, post_id):
        followers = self.followers.all()
        for follower in followers:
            redis_key = f'{follower.id}:feed'
            redis_instance.lpush(redis_key, str(post_id))
    
    def get_feed(self):
        redis_key = f'{self.id}:feed'
        post_ids = redis_instance.lrange(redis_key, 0, -1)
        decoded_ids = [id.decode('utf-8') for id in post_ids]
        return decoded_ids