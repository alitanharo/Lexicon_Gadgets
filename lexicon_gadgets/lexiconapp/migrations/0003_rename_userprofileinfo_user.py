# Generated by Django 4.1.2 on 2022-11-16 13:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lexiconapp', '0002_userprofileinfo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfileInfo',
            new_name='User',
        ),
    ]