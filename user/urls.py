from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('<int:pk>', views.UserProfile.as_view()),
    path('', include('followers.urls')),
    path('', views.GetUser.as_view(), name="get_user"),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', views.register),
    path('password', views.update_password, name="update_password"),
    path('profile/picture', views.UpdateProfilePicture.as_view(),
         name="update_profile_picture"),
]
