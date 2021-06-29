# Generated by Django 3.2.4 on 2021-06-29 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0011_alter_reactiontypes_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentreaction',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comment_reaction', to='user.user', verbose_name='Author'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postreaction',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='post_reaction', to='user.user', verbose_name='Author'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comments',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
    ]
