# Generated by Django 3.2.4 on 2021-06-24 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('followers', '0007_followrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followrequest',
            name='is_accepted',
        ),
    ]