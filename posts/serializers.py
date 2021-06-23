from rest_framework import serializers
from .models import Posts


class PostSerializer(serializers.Serializer):
    class Meta:
        model = Posts
