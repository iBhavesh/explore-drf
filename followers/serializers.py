from rest_framework import serializers
from .models import Followers


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = ['follower', 'following']
