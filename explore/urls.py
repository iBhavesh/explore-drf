from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('custom_auth.urls')),
    path('user/', include('user.urls')),
    path('posts/', include('posts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
