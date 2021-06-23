from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.


class Followers(models.Model):
    follower_id = models.ForeignKey("user.User", verbose_name=_(
        "Follower Id"), on_delete=models.CASCADE, related_name="follower")
    followee_Id = models.ForeignKey("user.User", verbose_name=_(
        "Followee id"), on_delete=models.CASCADE, related_name="followee")
    is_accepted = models.BooleanField(_("Is Accepted"), default=False)
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, default=timezone.now)
    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Followers"
        default_related_name = '%(model_name)s'
        get_latest_by = "-created_at"
