# Generated by Django 3.2.4 on 2021-07-08 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_posts_media_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Comments'},
        ),
    ]