from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Posts(models.Model):
    author = models.ForeignKey("user.User", verbose_name=_(
        "Author"), on_delete=models.CASCADE)
    text = models.TextField(_("Text"))
    media = models.FileField(_("media"), upload_to=None,
                             max_length=100, null=True)
    media_type = models.CharField(_("Media Type"), max_length=50, null=True)

    class Meta:
        verbose_name_plural = "Posts"


class Comments(models.Model):
    post = models.ForeignKey("posts.Posts", verbose_name=_(
        "Comments"), on_delete=models.CASCADE)
    is_active = models.BooleanField(_("Is Active"), default=True)
    comment = models.TextField(_("Comment"))

    class Meta:
        verbose_name_plural = "Comments"
