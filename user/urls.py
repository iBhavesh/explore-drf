from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('<int:pk>', views.UserProfile.as_view()),
    path('search', views.UserSearch.as_view()),
    path('forgot-password', views.ForgetPassword.as_view()),
    path('reset/password', views.ResetPassword.as_view()),
    path('<int:user_id>/posts', views.UserPostList.as_view()),
    path('', include('followers.urls')),
    path('', include('notifications.urls')),
    path('', views.GetUser.as_view(), name="get_user"),
    path('signin', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', views.register),
    path('password', views.update_password, name="update_password"),
    path('profile/picture', views.UpdateProfilePicture.as_view(),
         name="update_profile_picture"),
    path('profile/<int:pk>', views.UpdateProfile.as_view(),
         name="update_profile"),
    path('profile/picture/remove', views.RemoveProfilePicture.as_view(),
         name="remove_profile_picture"),
]
