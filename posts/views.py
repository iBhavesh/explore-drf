from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import PostSerializer

# Create your views here.


class AddPost(CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PostSerializer
