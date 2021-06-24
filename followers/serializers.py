from rest_framework import serializers
from user.serializers import UserSerializer
from .models import Followers


class FollowerSerializer(serializers.ModelSerializer):
    # follower = UserSerializer()
    # following = UserSerializer()

    class Meta:
        model = Followers
        fields = ['follower', 'following']
        depth = 2
