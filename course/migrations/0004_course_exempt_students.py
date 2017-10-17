# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-15 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20170807_1719'),
        ('course', '0003_course_disable_sync'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='exempt_students',
            field=models.ManyToManyField(to='school.Student'),
        ),
    ]