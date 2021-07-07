import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
from helpers import upload_to


class Posts(models.Model):
    content_option = [
        ('post', 'post'),
        ('profile', 'profile')
    ]
    media_type_options = [
        (None, None),
        ('video', 'video'),
        ('image', 'image'),
    ]

    author = models.ForeignKey(User, verbose_name=_(
        "Author"), on_delete=models.CASCADE, related_name="posts")
    caption = models.TextField(_("Caption"), blank=True)
    media = models.FileField(_("Media Path"), upload_to=upload_to,
                             max_length=255, null=True,)
    media_type = models.CharField(_("Media Type"), choices=media_type_options,
                                  max_length=50, null=True, blank=True)
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

    class Meta:
        verbose_name_plural = "Posts"
        ordering = ['-created_at']


class Comments(models.Model):
    author = models.ForeignKey(User, verbose_name=_(
        "Author"), on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Posts, verbose_name=_(
        "post"), on_delete=models.CASCADE)
    is_active = models.BooleanField(_("Is Active"), default=True)
    comment = models.TextField(_("Comment"))
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Comments"
        ordering = ['-created_at']


class ReactionTypes(models.Model):
    ## Like, Love, Laugh, Want

    reaction_type = models.CharField(_("Reaction Type"), max_length=50)

    def __str__(self):
        return self.reaction_type

    class Meta:
        verbose_name_plural = "ReactionTypes"
        ordering = ['id']


class PostReaction(models.Model):
    author = models.ForeignKey(User, verbose_name=_(
        "Author"), on_delete=models.CASCADE, related_name="post_reaction")
    post = models.ForeignKey(Posts, verbose_name=_("post"),
                             on_delete=models.CASCADE,
                             related_name="post_reaction")
    reaction_type = models.ForeignKey(
        ReactionTypes, verbose_name=_("Reaction"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name_plural = "PostReactions"
        unique_together = ('author', 'post')


class CommentReaction(models.Model):
    author = models.ForeignKey(User, verbose_name=_(
        "Author"), on_delete=models.CASCADE, related_name="comment_reaction")
    comment = models.ForeignKey(Comments, verbose_name=_("comment"),
                                on_delete=models.CASCADE,
                                related_name="comment_reaction")
    reaction_type = models.ForeignKey(
        ReactionTypes, verbose_name=_("Reaction"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name_plural = "CommentReactions"
        unique_together = ('author', 'comment')
