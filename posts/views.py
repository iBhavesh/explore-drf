from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
)
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, DestroyModelMixin)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from .permissions import IsAuthorOrPostAuthorOrReadOnly, IsAuthorOrReadOnly
from .serializers import (
    CommentReactionSerializer,
    CommentSerializer,
    PostListSerializer, PostReactionSerializer, PostSerializer
)
from .models import CommentReaction, Comments, PostReaction, Posts

# Create your views here.


class PostList(ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostListSerializer
        return PostSerializer

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
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostListSerializer
        return PostSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Posts.objects.filter(~Q(author=user_id),
                                    Q(author__is_private_profile=False) |
                                    Q(author__followed_by=user_id))


class CommentList(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.all()

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        request.data['post'] = kwargs['post_id']
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        comments = queryset.filter(post=kwargs['post_id'])
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Comment(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrPostAuthorOrReadOnly]

    def get_queryset(self):
        return Comments.objects.filter(post=self.kwargs['post_id'])

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class PostReactionList(GenericAPIView, ListModelMixin, CreateModelMixin, DestroyModelMixin):
    serializer_class = PostReactionSerializer

    def get_queryset(self):
        return PostReaction.objects.filter(post=self.kwargs['post_id'])

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        request.data['post'] = kwargs['post_id']
        print(request.data)
        return super().create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(),
                                     author=self.request.user.id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# class PostReactionRemove(APIView, DestroyModelMixin):
#     def get_queryset(self):
#         return PostReaction.objects.filter(post=self.kwargs['post_id'],
#                                            author=self.request.user.id)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

#     def destroy(self, request, *args, **kwargs):
#         instance = get_object_or_404(self.get_queryset(),
#                                               author=self.request.user.id)
#         self.perform_destroy(instance)


class CommentReactionList(GenericAPIView, ListModelMixin, CreateModelMixin, DestroyModelMixin):
    serializer_class = CommentReactionSerializer

    def get_queryset(self):
        return CommentReaction.objects.filter(comment=self.kwargs['comment_id'])

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        request.data['comment'] = kwargs['comment_id']
        print(request.data)
        return super().create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(),
                                     author=self.request.user.id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# class CommentReactionRemove(APIView, DestroyModelMixin):
#     def get_queryset(self):
#         return CommentReaction.objects.filter(comment=self.kwargs['comment_id'])

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

#     def destroy(self, request, *args, **kwargs):
#         instance = get_object_or_404(self.get_queryset(),
#                                               author=self.request.user.id)
#         self.perform_destroy(instance)
