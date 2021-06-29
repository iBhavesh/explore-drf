from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name="post_list"),
    path('<int:pk>', views.Post.as_view(), name="RUD_post"),
    path('<int:post_id>/react', views.ReactPost.as_view(), name="post_react_list"),
    path('<int:post_id>/comments', views.CommentList.as_view(),
         name="comment_list"),
    path('<int:post_id>/comments/<int:pk>', views.Comment.as_view(),
         name="RUD_comment"),
]
