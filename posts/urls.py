from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name="post_list"),
    path('<int:pk>', views.Post.as_view(), name="RUD_post"),
    path('<int:post_id>/comments', views.CommentList.as_view(),
         name="comment_list"),
    path('<int:post_id>/comments/<int:pk>', views.Comment.as_view(),
         name="RUD_comment"),
    path('<int:post_id>/reaction', views.PostReactionList.as_view(),
         name="post_reaction_list"),
    #     path('<int:post_id>/reaction/<int:pk>', views.PostReactionRemove.as_view(),
    #          name="del_post_reaction"),
    path('<int:post_id>/comments/<int:comment_id>/reaction',
         views.CommentReactionList.as_view(),
         name="comment_reaction"),
    #     path('<int:post_id>/comments/<int:comment_id>/reaction/<int:pk>',
    #          views.CommentReactionRemove.as_view(),
    #          name="del_comment_reaction"),
]
