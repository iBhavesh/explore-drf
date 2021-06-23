from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User


class Posts(models.Model):
    content_option = [
        ('post', 'post'),
        ('profile', 'profile')
    ]

    author = models.ForeignKey(User, verbose_name=_(
        "Author"), on_delete=models.CASCADE)
    caption = models.TextField(_("Caption"))
    media_path = models.FileField(_("Media Path"), upload_to='posts',
                                  max_length=255, null=True)
    media_type = models.CharField(_("Media Type"), max_length=50, null=True)
    content_type = models.CharField(
        _("Content type"), max_length=50, choices=content_option)
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.caption[:10] + "..."

    class Meta:
        verbose_name_plural = "Posts"


class Comments(models.Model):
    post = models.ForeignKey(Posts, verbose_name=_(
        "Comments"), on_delete=models.CASCADE)
    is_active = models.BooleanField(_("Is Active"), default=True)
    comment = models.TextField(_("Comment"))
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Comments"
