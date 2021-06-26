from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Comments, Posts

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ['caption', 'media_type',
                  'content_type', 'media', 'author']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ['post', 'comment', 'created_at']
        extra_kwargs = {'is_active': {'write_only': True}}
