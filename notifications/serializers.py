from rest_framework import serializers
from .models import Notifications
from user.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer()

    class Meta:
        model = Notifications
        fields = ['id', 'owner', 'actor', 'type', 'post', 'read', 'created_at']
        # depth = 1
