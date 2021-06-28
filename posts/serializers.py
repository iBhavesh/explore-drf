from django.contrib.auth import get_user_model
from rest_framework import serializers
from user.serializers import UserSerializer
from .models import Comments, Posts

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Posts
        fields = ['id', 'author', 'caption', 'media_type',
                  'content_type', 'media', 'created_at']
        depth: 1


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ['post', 'comment', 'created_at']
        extra_kwargs = {'is_active': {'write_only': True}}
