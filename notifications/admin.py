from django.contrib import admin
from .models import Notifications


@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ["owner", "id", "post", "type", "actor", "created_at"]
