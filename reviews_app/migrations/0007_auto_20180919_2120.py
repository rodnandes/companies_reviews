# Generated by Django 2.1.1 on 2018-09-19 21:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews_app', '0006_auto_20180919_1807'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('company', 'reviewer')},
        ),
    ]