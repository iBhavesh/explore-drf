from django.contrib import admin
from .models import Posts, Comments, ReactionTypes, PostReaction, CommentReaction
# Register your models here.


@admin.register(Posts)
class PostsManager(admin.ModelAdmin):
    list_display = ['author', 'id', 'caption',
                    'media_type', 'content_type', 'created_at']


@admin.register(Comments)
class CommentsManager(admin.ModelAdmin):
    list_display = ['author', 'id', 'post',
                    'comment', 'created_at', 'updated_at', 'is_active']


@admin.register(ReactionTypes)
class ReactionManager(admin.ModelAdmin):
    list_display = ['reaction_type', 'id']


@admin.register(PostReaction)
class PostReactionManager(admin.ModelAdmin):
    list_display = ['reaction_type', 'id', 'post', 'author']


@admin.register(CommentReaction)
class CommentReactionManager(admin.ModelAdmin):
    list_display = ['reaction_type', 'id', 'comment', 'author']
