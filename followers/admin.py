from django.contrib import admin
from .models import Followers
# Register your models here.

# admin.site.register(Followers)


@admin.register(Followers)
class FollowersAdmin(admin.ModelAdmin):
    list_display = ("follower", "following", "is_accepted", "id")
