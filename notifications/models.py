from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
from posts.models import Posts


class Notifications(models.Model):
    notification_type = [
        ('comment', 'comment'),
        ('post_reaction', 'post_reaction'),
        ('comment_reaction', 'comment_reaction'),
    ]

    owner = models.ForeignKey(User, verbose_name=_("Owner"),
                              on_delete=models.CASCADE,
                              related_name="notifications")
    actor = models.ForeignKey(User, verbose_name=_("Actor"),
                              on_delete=models.CASCADE,
                              related_name="notification_actor")
    type = models.CharField(_("Type"), max_length=50,
                            choices=notification_type)
    post = models.ForeignKey(Posts, verbose_name=_(
        "post"), on_delete=models.CASCADE)
    read = models.BooleanField(_("Read"), default=False)
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']
