# Generated by Django 3.2.4 on 2021-07-08 23:04

from django.db import migrations, models
import django.utils.timezone
import helpers


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_comments_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='media',
            field=models.FileField(default=django.utils.timezone.now, max_length=255, upload_to=helpers.upload_to, verbose_name='Media Path'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='posts',
            name='media_type',
            field=models.CharField(blank=True, choices=[(None, None), ('video', 'video'), ('image', 'image')], default='image', max_length=50, verbose_name='Media Type'),
            preserve_default=False,
        ),
    ]
