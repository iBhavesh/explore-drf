from time import strftime
import os
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from user.models import User


def upload_to(instance, filename):
    print(instance, filename)
    filenames = os.path.splitext(filename)
    return "posts/" + strftime('%Y%m%d%H%M%S') + filenames[-1]


class Posts(models.Model):
    content_option = [
        ('post', 'post'),
        ('profile', 'profile')
    ]
    media_type_options = [
        ('video', 'video/*'),
        ('image', 'image/*'),
    ]

    author = models.ForeignKey(User, verbose_name=_(
        "Author"), on_delete=models.CASCADE)
    caption = models.TextField(_("Caption"), blank=True)
    media = models.FileField(_("Media Path"), upload_to=upload_to,
                             max_length=255, null=True,)
    media_type = models.CharField(_("Media Type"), max_length=50, null=True)
    content_type = models.CharField(
        _("Content type"), max_length=50, choices=content_option)
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=True, auto_now_add=False)

    def __str__(self):
        if len(self.caption) > 0:
            return self.caption[:10] + "..."
        return self.author.first_name + "'s Upload"

    def delete(self, using, keep_parents):
        try:
            os.remove(self.media)
        except:  # pylint: disable=bare-except
            print('File Could not be deleted')
        return super().delete(using=using, keep_parents=keep_parents)

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.media = self.compressImage(self.uploadedImage)
    #     super().save(*args, **kwargs)

    def compressImage(self, uploadedImage):
        imageTemproary = Image.open(uploadedImage)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((1020, 573))
        imageTemproary.save(outputIoStream, format='JPEG', quality=60)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[
                                             0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage

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
