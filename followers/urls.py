from django.urls import path
from . import views
urlpatterns = [
    path("<int:pk>/following", views.get_following, name="get-following"),
    path("<int:pk>/followers", views.get_follower, name="get-followers"),
    path("follower/remove", views.RemoveFollower.as_view(), name="remove-follower"),
    path("follower/unfollow", views.UnFollow.as_view(),
         name="unfollow-follower"),
    path("follower/<int:follower_id>/accept",
         views.accept_follower, name="accept-follower"),
    path("follower/<int:follower_id>/reject",
         views.reject_follow_request, name="reject-follower"),
    path("follower/send-request", views.SendFollowRequest.as_view(),
         name="send-follow-request"),
]
