from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Like
from posts.models import Post

@api_view(['POST'])
def create_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # Check if the user has already liked the post
    if Like.objects.filter(user=request.user, post=post).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    like = Like(user=request.user, post=post)
    like.save()
    # return like_id so user can remove like if wanted
    return Response({"like_id": like.id}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def delete_like(request, like_id):
    # Check if the like exists
    try:
        like = Like.objects.get(pk=like_id, user=request.user)
    except Like.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    like.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)