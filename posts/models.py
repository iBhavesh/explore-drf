from time import strftime
import mimetypes
import os
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from user.models import User


def upload_to(instance, filename):
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

    def save(self, *args, **kwargs):
        if not self.id:
            self.media = self.compress_image(self.media)
        super().save(*args, **kwargs)

    def compress_image(self, uploaded_image):
        mime_type = mimetypes.guess_type(uploaded_image.name)
        if mime_type[0] is not None:
            return uploaded_image
        elif not mime_type[0].startswith('image'):
            return uploaded_image
        elif uploaded_image.size is not None and uploaded_image.size / 1024 < 200:
            return uploaded_image
        image_temporary = Image.open(uploaded_image)
        output_io_stream = BytesIO()
        # imageTemproaryResized = imageTemproary.resize((1020, 573))
        image_temporary.save(output_io_stream, format='JPEG', quality=50)
        output_io_stream.seek(0)
        uploaded_image = InMemoryUploadedFile(
            output_io_stream, 'ImageField', "%s.jpg" % uploaded_image.name.split('.')[
                0], 'image/jpeg', sys.getsizeof(output_io_stream), None)
        return uploaded_image

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
