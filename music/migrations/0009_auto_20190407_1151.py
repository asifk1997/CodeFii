# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2019-04-07 06:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0008_album_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_output', models.FileField(default='', upload_to='')),
                ('verdict', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='song',
            name='problem_expected_output',
            field=models.FileField(default='', upload_to=''),
        ),
        migrations.AddField(
            model_name='song',
            name='problem_input',
            field=models.FileField(default='', upload_to=''),
        ),
        migrations.AddField(
            model_name='submission',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Song'),
        ),
        migrations.AddField(
            model_name='submission',
            name='username',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
