from django.http import FileResponse, HttpResponseNotFound
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from posts.models import Posts


class GetFile(APIView):
    def get(self, request, file_path):

        if not request.user.is_superuser:
            post = Posts.objects.filter(media=file_path)
            if not post.exists():
                return HttpResponseNotFound()
            if request.user.id is not post[0].author.id:
                print(request.user)
                post = Posts.objects.filter(media=file_path,
                                            author__id__in=request.user.follows.values('id'))
                if not post.exists():
                    return Response({"error": '''File is private
                     Only people who follow the user can view this file'''},
                                    status=HTTP_404_NOT_FOUND)

        response = FileResponse(open(settings.MEDIA_ROOT / file_path, 'rb'))
        return response
