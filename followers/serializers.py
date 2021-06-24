from rest_framework import serializers
from user.serializers import UserSerializer
from .models import FollowRequest, Followers


class FollowerSerializer(serializers.ModelSerializer):
    follower = UserSerializer()
    following = UserSerializer()

    class Meta:
        model = Followers
        fields = ['follower', 'following']
        depth = 0


class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRequest
        fields = ['request_from', 'request_to']
