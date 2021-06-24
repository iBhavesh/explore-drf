from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from user.models import User

# Create your models here.


class RelationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_accepted=True)


class Followers(models.Model):
    follower = models.ForeignKey(User, verbose_name=_(
        "Follower"), on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, verbose_name=_(
        "Following"), on_delete=models.CASCADE, related_name="follower")
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, default=timezone.now)
    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.follower.email + " " + self.following.email

    class Meta:
        verbose_name_plural = "Followers"
        unique_together = ('follower', 'following')


class FollowRequest(models.Model):
    request_from = models.ForeignKey(User, verbose_name=_(
        "Request From"), on_delete=models.CASCADE, related_name='req_from')
    request_to = models.ForeignKey(User, verbose_name=_(
        "Request To"), on_delete=models.CASCADE, related_name='req_to')
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, default=timezone.now)
    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Follow Requests"
        unique_together = ('request_from', 'request_to')
