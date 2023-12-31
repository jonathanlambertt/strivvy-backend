from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'description', 'title', 'thumbnail', 'favicon', 'site_name', 'url')
        read_only_fields = ('id', 'user')
    
    def create(self, validated_data):
        # Add the current user to the validated data before creating the Post instance
        validated_data['user'] = self.context['request'].user
        post = Post.objects.create(**validated_data)
        return post
