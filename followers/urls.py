from django.urls import path
from . import views
urlpatterns = [
    path("<int:pk>/following", views.get_following, name="get-following"),

    path("<int:pk>/followers", views.get_follower, name="get-followers"),

    path("<int:pk>/follower/remove",
         views.RemoveFollower.as_view(), name="remove-follower"),

    path("<int:pk>/following/unfollow", views.UnFollow.as_view(),
         name="unfollow-follower"),

    path("<int:follower_id>/follower/accept",
         views.accept_follower, name="accept-follower"),

    path("<int:follower_id>/follower/reject",
         views.reject_follow_request, name="reject-follower"),

    path("<int:pk>/follow/request", views.SendFollowRequest.as_view(),
         name="send-follow-request"),

    path("<int:pk>/follow/request/cancel", views.CancelFollowRequest.as_view(),
         name="cancel-follow-request"),

    path("<int:pk>/follow/status", views.FollowStatus.as_view(),
         name="follow status"),

    path("follow/requests", views.FollowRequests.as_view(),
         name="get-follow-request"),
]
