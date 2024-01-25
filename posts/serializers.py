from rest_framework import serializers
from .models import Post
from likes.models import Like

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

class FeedPostSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    is_liked = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'username', 'user_id', 'url', 'date', 'description', 'title', 'thumbnail', 'favicon', 'site_name', 'is_liked', 'like_id')
    
    def get_is_liked(self, obj):
        user = self.context['request'].user
        return Like.objects.filter(user=user, post=obj).exists()

    def get_like_id(self, obj):
        user = self.context['request'].user
        like = Like.objects.filter(user=user, post=obj).first()
        return like.id if like else None