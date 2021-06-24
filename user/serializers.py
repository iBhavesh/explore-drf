from rest_framework import serializers
from .models import User


class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name',
                  'last_name']


class UserSerializer(serializers.ModelSerializer):
    follows = NestedUserSerializer(read_only=True, many=True)
    # follower = NestedUserSerializer(read_only=True, many=True)
    # following = NestedUserSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'date_of_birth', 'follows', 'follower', 'following']
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
