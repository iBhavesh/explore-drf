from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import User
# Create your views here.


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.data['email'])
            refresh_token = RefreshToken.for_user(user)
            data = {
                'access': str(refresh_token.access_token),
                'refresh': str(refresh_token)
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response('Perhaps something went wrong', status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_password(request):
    try:
        user = User.objects.get(pk=request.user.id)
        password_is_valid = check_password(
            request.data['password'], user.password)
        if password_is_valid:
            if request.data['new_password'] == request.data['confirm_password']:
                print(user.password)
                user.set_password(request.data['new_password'])
                user.save()
                print(user.password)
                return Response('Updated', status=status.HTTP_200_OK)
            return Response('Password and confirm password should match', status=status.HTTP_400_BAD_REQUEST)
        return Response('Incorrect Password', status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response('Request parameter are invalid', status=status.HTTP_400_BAD_REQUEST)
