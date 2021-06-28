from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name="post_list"),
    path('<int:pk>', views.Post.as_view(), name="post_retrieve_update_destroy"),
]
