from django.urls import path
from . import views
urlpatterns = [
    path("user/following/<int:pk>", views.get_following, name="get-followers"),
    path("followers/<int:pk>/accept",
         views.accept_follower, name="accept-follower"),
    path("followers/send-request", views.SendFollowRequest.as_view(),
         name="send-follow-request"),
]
