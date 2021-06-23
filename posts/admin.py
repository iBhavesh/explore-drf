from django.contrib import admin
from .models import Posts, Comments
# Register your models here.


@admin.register(Posts)
class PostsManager(admin.ModelAdmin):
    pass


@admin.register(Comments)
class CommentsManager(admin.ModelAdmin):
    pass
