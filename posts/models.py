import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
from helpers import compress_image, upload_to


class Posts(models.Model):
    content_option = [
        ('post', 'post'),
        ('profile', 'profile')
    ]
    media_type_options = [
        (None, None),
        ('video', 'video/*'),
        ('image', 'image/*'),
    ]

    author = models.ForeignKey(User, verbose_name=_(
        "Author"), on_delete=models.CASCADE, related_name="posts")
    caption = models.TextField(_("Caption"), blank=True)
    media = models.FileField(_("Media Path"), upload_to=upload_to,
                             max_length=255, null=True,)
    media_type = models.CharField(_("Media Type"), choices=media_type_options,
                                  max_length=50, null=True)
    content_type = models.CharField(
        _("Content type"), max_length=50, choices=content_option)
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.id)

    def delete(self, *args, **kwargs):
        try:
            os.remove(self.media)
        except:  # pylint: disable=bare-except
            print('File Could not be deleted')
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.content_type == 'profile':
            self.media_type = 'image'
        if not self.id:
            if self.media.path is not None:
                self.media = compress_image(self.media)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Posts"
        ordering = ['-created_at']


class Comments(models.Model):
    author = models.ForeignKey(User, verbose_name=_(
        "Author"), on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, verbose_name=_(
        "post"), on_delete=models.CASCADE)
    is_active = models.BooleanField(_("Is Active"), default=True)
    comment = models.TextField(_("Comment"))
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Comments"
        ordering = ['created_at']
