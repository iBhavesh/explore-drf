# Generated by Django 3.2.4 on 2021-06-23 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('followers', '0004_rename_followee_id_followers_followee_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='followers',
            old_name='followee_id',
            new_name='followee',
        ),
        migrations.RenameField(
            model_name='followers',
            old_name='follower_id',
            new_name='follower',
        ),
    ]