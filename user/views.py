from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView
from posts.models import Posts
from posts.serializers import PostListSerializer, PostSerializer
from .serializers import MyTokenObtainPairSerializer, UserSerializer
from .models import PasswordReset, User
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
                user.set_password(request.data['new_password'])
                user.save()
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


class UpdateProfile(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class RemoveProfilePicture(APIView):

    def delete(self, request):
        request.user.profile_picture = None
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfile(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSearch(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        query_string = self.request.GET.get('query', '').split()
        print(query_string)
        queryset = User.objects.filter(Q(email__in=query_string) |
                                       Q(first_name__in=query_string) |
                                       Q(last_name__in=query_string))
        return queryset


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


class ForgetPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        user = User.objects.filter(email=request.data.get("email", ""))
        if not user.exists():
            return Response({"error": "User with this email not found"},
                            status=status.HTTP_400_BAD_REQUEST)
        reset_token = get_random_string(
            length=6, allowed_chars="ABCDEFGHJKMNPQRSTUVWXYS123456789")
        print(reset_token)
        pr = PasswordReset.objects.filter(user_id=user[0].id)
        if pr.exists():
            pr[0].delete()
        PasswordReset.objects.create(
            user_id=user[0],
            verification_key=reset_token
        )
        send_mail("Password Reset", "Your Password reset token is " + reset_token,
                  "no-reply@explore.com",
                  [user[0].email])
        return Response("Password reset token created", status=status.HTTP_201_CREATED)


class ResetPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def put(self, request):
        reset_token = request.data.get("reset_token", "")
        password = request.data.get("password", "")
        print(password)
        password_reset = PasswordReset.objects.filter(
            verification_key=reset_token)
        if not password_reset.exists():
            return Response("Token Not Valid", status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=password_reset[0].user_id.id)
        except User.DoesNotExist:
            return Response("User not Found", status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        password_reset[0].delete()
        return Response("New password set", status=status.HTTP_201_CREATED)
