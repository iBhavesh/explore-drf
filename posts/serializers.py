from django.contrib.auth import get_user_model
from rest_framework import serializers
from user.serializers import UserSerializer
from .models import CommentReaction, Comments, PostReaction, Posts

User = get_user_model()


class PostReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostReaction
        fields = ['author', 'post', 'reaction_type', 'created_at']
        # depth = 1


class CommentReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentReaction
        fields = ['author', 'comment', 'reaction_type', 'created_at']


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    post_reaction = PostReactionSerializer(many=True, read_only=True)

    class Meta:
        model = Posts
        fields = ['id', 'author', 'caption', 'media_type',
                  'content_type', 'media', 'post_reaction', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    post_reaction = PostReactionSerializer(many=True, read_only=True)

    class Meta:
        model = Posts
        fields = ['id', 'author', 'caption', 'media_type',
                  'content_type', 'media', 'post_reaction', 'created_at']


class CommentPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ['id', 'author']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ['id', 'author', 'post', 'comment', 'created_at']
        extra_kwargs = {'is_active': {'write_only': True}}


class CommentListSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    comment_reaction = CommentReactionSerializer(many=True, read_only=True)
    post = CommentPostSerializer()

    class Meta:
        model = Comments
        fields = ['id', 'author', 'post', 'comment',
                  'created_at', 'comment_reaction']
        extra_kwargs = {'is_active': {'write_only': True}}
