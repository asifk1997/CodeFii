# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2019-04-09 14:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0014_auto_20190409_1925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='audio_file',
            new_name='problem_file',
        ),
    ]
