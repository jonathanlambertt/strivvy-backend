from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from django.core.validators import MaxLengthValidator

from .models import User
from posts.models import Post

class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="That email is already in use.")]
    )

    password = serializers.CharField(
        write_only=True,
        min_length=6,
        error_messages={
            'min_length': 'Your password must be at least 6 characters.'
        }
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        user.following.add(user)
        Token.objects.create(user=user)
        return user

class UserSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    is_searching_user = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'is_following', 'is_searching_user']  # Add more fields as needed

    def get_is_following(self, obj):
        request = self.context.get('request')
        user = request.user if request else None

        # Check if the current user is following the user in the serializer
        if user and user.is_authenticated:
            return user.following.filter(id=obj.id).exists()

        return False
    
    def get_is_searching_user(self, obj):
        request = self.context.get('request')
        user = request.user if request else None

        # Check if the user being searched is the same as the user performing the search
        if user and user.is_authenticated:
            return user.id == obj.id

        return False

class ProfileSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'post_count', 'following_count']
    
    def get_post_count(self, obj):
        return Post.objects.filter(user=obj).count()

    def get_following_count(self, obj):
        return obj.following.exclude(pk=obj.pk).count()