from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.urls.conf import include
from .import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('posts/', include('posts.urls')),
    path(str(settings.MEDIA_URL)[1:] +
         "<path:file_path>", views.GetFile.as_view())
]
