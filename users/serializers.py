from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from django.core.validators import MaxLengthValidator

from .models import User

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
        Token.objects.create(user=user)
        return user
