from rest_framework import serializers
from posts.models import Posts
from .models import User


class NestedFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name']


class NestedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['caption', 'media_type',
                  'content_type', 'media']


class UserProfileSerializer(serializers.ModelSerializer):
    # follows = NestedFollowSerializer(read_only=True, many=True)
    # followed_by = NestedFollowSerializer(read_only=True, many=True)
    # posts = NestedPostSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'date_of_birth', 'follows',
                  'followed_by', 'profile_picture', 'posts']
        extra_kwargs = {'password': {'write_only': True}}
        depth = 0

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            password=validated_data['password'],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'date_of_birth',  'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            password=validated_data['password'],
        )
        return user
