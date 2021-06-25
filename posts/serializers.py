from rest_framework import serializers
from .models import Comments, Posts


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['author', 'caption', 'media_type',
                  'content_type', 'media']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ['post', 'comment', 'created_at']
        extra_kwargs = {'is_active': {'write_only': True}}
