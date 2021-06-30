from django.http import FileResponse
from django.conf import settings
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED)
from posts.models import Posts
from .models import MediaLink


class GetFileURL(APIView):
    def get(self, request, file_path):
        print(file_path)

        post = Posts.objects.filter(media=file_path)
        print(file_path)
        if not post.exists():
            return Response({"error": "File Not Found"},
                            status=HTTP_404_NOT_FOUND)
        if request.user.is_superuser:
            return FileResponse(
                open(settings.MEDIA_ROOT / file_path, 'rb'))
        if request.user.id is not post[0].author.id:
            media_link = MediaLink.objects.create(file_path=file_path)
            url = reverse("media_url", args=(media_link.id,))
            return Response({"url": url}, status=HTTP_201_CREATED)
        if post[0].author.is_private_profile:
            if request.user.follows is not post[0].author:
                return Response({"error": "File is private."
                                 "Only people who follow the user"
                                 " can view this file"},
                                status=HTTP_401_UNAUTHORIZED)

        media_link = MediaLink.objects.create(file_path=file_path)
        url = reverse("media_url", args=(media_link.id,))
        return Response({"url": url}, status=HTTP_201_CREATED)


class GetFile(APIView):
    def get(self, request, pk):
        try:
            media_link = MediaLink.objects.get(pk=pk)
        except MediaLink.DoesNotExist:
            return Response({"error": "File Not Found"},
                            status=HTTP_404_NOT_FOUND)
        file_path = media_link.file_path
        media_link.delete()
        return FileResponse(
            open(settings.MEDIA_ROOT / file_path, 'rb'))
