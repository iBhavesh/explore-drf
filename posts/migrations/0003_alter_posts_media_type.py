# Generated by Django 3.2.4 on 2021-06-30 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='media_type',
            field=models.CharField(blank=True, choices=[(None, None), ('video', 'video'), ('image', 'image')], max_length=50, null=True, verbose_name='Media Type'),
        ),
    ]
