from django.contrib import admin
from .models import FollowRequest, Followers
# Register your models here.

# admin.site.register(Followers)


@admin.register(Followers)
class FollowersAdmin(admin.ModelAdmin):
    list_display = ("follower", "following")


@admin.register(FollowRequest)
class FollowRequestsAdmin(admin.ModelAdmin):
    list_display = ("request_from", "request_to")
