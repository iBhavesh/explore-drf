# Generated by Django 3.2.4 on 2021-06-29 08:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0012_auto_20210629_0751'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='commentreaction',
            unique_together={('author', 'comment')},
        ),
        migrations.AlterUniqueTogether(
            name='postreaction',
            unique_together={('author', 'post')},
        ),
    ]
