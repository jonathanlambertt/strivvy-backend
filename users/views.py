from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import User
from posts.models import Post
from posts.serializers import FeedPostSerializer
from .serializers import CreateUserSerializer, UserSerializer, ProfileSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    if request.method == 'POST':
        user_serializer = CreateUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def follow_user(request, user_id):
    current_user = request.user
    user_to_follow = get_object_or_404(User, id=user_id)

    # check if user is already following target user
    if current_user.following.filter(id=user_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    current_user.following.add(user_to_follow)
    current_user.save()
    return Response(status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def unfollow_user(request, user_id):
    current_user = request.user
    user_to_unfollow = get_object_or_404(User, id=user_id)

    # check if user is not following the target user
    if not current_user.following.filter(id=user_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    current_user.following.remove(user_to_unfollow)
    current_user.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def search_for_user(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query)
    serializer = UserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_profile(request):
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
def get_feed(request):
    post_ids = request.user.get_feed()
    posts = []
    for id in post_ids:
        posts.append(Post.objects.get(id=id))
    serializer = FeedPostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)