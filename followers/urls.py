from django.urls import path
from . import views
urlpatterns = [
    path("user/following/<int:pk>", views.get_following, name="get-following"),
    path("user/followers/<int:pk>", views.get_follower, name="get-followers"),
    path("followers/<int:pk>/accept",
         views.accept_follower, name="accept-follower"),
    path("followers/send-request", views.SendFollowRequest.as_view(),
         name="send-follow-request"),
]
