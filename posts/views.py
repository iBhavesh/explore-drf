from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from posts.permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer
from .models import Posts

# Create your views here.


class PostList(ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Posts.objects.filter(~Q(author=user_id),
                                    Q(author__is_private_profile=False) |
                                    Q(author__followed_by=user_id))

    def create(self, request, *args, **kwargs):
        author = request.data.get('author', "")
        if request.user.id is not int(author):
            return Response({"error": "You are not authorized to do this"},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().create(request, *args, **kwargs)


class Post(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        user_id = self.request.user.id
        return Posts.objects.filter(~Q(author=user_id),
                                    Q(author__is_private_profile=False) |
                                    Q(author__followed_by=user_id))
