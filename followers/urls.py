from django.urls import path
from . import views
urlpatterns = [
    path("<int:pk>", views.get_followers, name="get-followers"),
    path("<int:pk>/accept", views.accept_follower, name="accept-follower"),
    path("send-request", views.SendFollowRequest.as_view(),
         name="send-follow-request"),
]
