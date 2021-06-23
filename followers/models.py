from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from user.models import User

# Create your models here.


class Followers(models.Model):
    follower = models.ForeignKey(User, verbose_name=_(
        "Follower"), on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, verbose_name=_(
        "Following"), on_delete=models.CASCADE, related_name="following")
    is_accepted = models.BooleanField(_("Is Accepted"), default=False)
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, default=timezone.now)
    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=True, auto_now_add=False)

    # def __str__(self):
    #     return self.follower.email + " " + self.followee.email

    class Meta:
        verbose_name_plural = "Followers"
        get_latest_by = "-created_at"
        unique_together = ('follower', 'following')
