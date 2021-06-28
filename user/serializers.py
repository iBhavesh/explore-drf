from rest_framework import serializers
from posts.models import Posts
from .models import User


class NestedUserSerializer(serializers.ModelSerializer):
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
    # follows = NestedUserSerializer(read_only=True, many=True)
    # followed_by = NestedUserSerializer(read_only=True, many=True)
    # posts = NestedPostSerializer(read_only=True, many=True)
    # request_from = NestedUserSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'date_of_birth', 'follows',
                  'followed_by', 'profile_picture', 'posts', 'follower', 'following']
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'date_of_birth',
                  'profile_picture', 'password', 'is_private_profile']
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )
        return user
