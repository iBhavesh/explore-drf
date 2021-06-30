from django.db import models
from django.utils.translation import gettext_lazy as _


class MediaLink(models.Model):
    file_path = models.CharField(_("File Path"), max_length=255)
