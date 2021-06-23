# Generated by Django 3.2.4 on 2021-06-23 22:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('followers', '0005_auto_20210623_2149'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='followers',
            options={'get_latest_by': '-created_at', 'verbose_name_plural': 'Followers'},
        ),
        migrations.AddField(
            model_name='followers',
            name='following',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='following', to='user.user', verbose_name='Following'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='followers',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Follower'),
        ),
        migrations.AlterUniqueTogether(
            name='followers',
            unique_together={('follower', 'following')},
        ),
        migrations.RemoveField(
            model_name='followers',
            name='followee',
        ),
    ]
