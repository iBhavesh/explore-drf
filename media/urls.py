from django.conf import settings
from django.urls import path
from .import views


urlpatterns = [
    path(str(settings.MEDIA_URL)[1:] +
         "<path:file_path>", views.GetFileURL.as_view()),
    path("media/<int:pk>", views.GetFile.as_view(), name="media_url")
]
