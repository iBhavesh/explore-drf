from django.http import FileResponse
from django.conf import settings
from rest_framework.views import APIView


class GetFile(APIView):
    def get(self, request, file_path):
        response = FileResponse(open(settings.MEDIA_ROOT / file_path, 'rb'))
        return response
