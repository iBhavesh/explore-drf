from django.http import FileResponse
from explore.settings import MEDIA_ROOT
from django.conf import settings
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import PostSerializer

# Create your views here.


class AddPost(CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PostSerializer
