from django.db.models import Q
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Posts

# Create your views here.


class AddPost(ListCreateAPIView):
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

    # def perform_create(self, serializer):
    #     if self.request.data['author'] is not self.request.user.id:
    #         raise ValidationError("You are not authorized to do this")
    #     serializer.save(author=self.request.user)
