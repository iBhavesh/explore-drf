# Generated by Django 3.2.4 on 2021-06-28 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('followers', '0010_auto_20210628_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='followers',
            name='is_accepted',
            field=models.BooleanField(default=False, verbose_name='Is Accepted'),
        ),
        migrations.DeleteModel(
            name='FollowRequest',
        ),
    ]
