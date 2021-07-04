from django.contrib.auth.hashers import check_password
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView
from posts.models import Posts
from posts.serializers import PostListSerializer, PostSerializer
from .serializers import MyTokenObtainPairSerializer, UserSerializer
from .models import User
# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message': 'Created Successfully'
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
            return Response('Password and confirm password should match',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response('Incorrect Password', status=status.HTTP_401_UNAUTHORIZED)
    except:  # pylint: disable=bare-except
        return Response('Request parameter are invalid', status=status.HTTP_400_BAD_REQUEST)


class UpdateProfilePicture(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        print(request.data)
        author = request.data.get('author', "")
        if request.user.id is not int(author):
            return Response({"error": "You are not authorized to do this"},
                            status=status.HTTP_401_UNAUTHORIZED)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(id=request.user.id)
            post = Posts.objects.filter(author=user.id)
            user.profile_picture = post[0].media
            user.profile_updated_at = post[0].updated_at
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GetUser(APIView):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserPostList(ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        if self.request.user.id == self.kwargs['user_id']:
            return Posts.objects.filter(Q(author=self.kwargs['user_id']))
        return Posts.objects.filter(Q(author=self.kwargs['user_id']),
                                    Q(author__is_private_profile=False) |
                                    Q(author__followed_by=self.kwargs['user_id']))
