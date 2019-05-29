# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2019-04-09 13:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0013_auto_20190408_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_title', models.CharField(max_length=250)),
                ('audio_file', models.FileField(default='', upload_to='')),
                ('problem_expected_output', models.FileField(default='', upload_to='')),
                ('is_favorite', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Problemset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curator', models.CharField(max_length=250)),
                ('problemset_title', models.CharField(max_length=500)),
                ('problemset_type', models.CharField(max_length=100)),
                ('problemset_logo', models.FileField(upload_to='')),
                ('is_favorite', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='album',
            name='user',
        ),
        migrations.RemoveField(
            model_name='song',
            name='album',
        ),
        migrations.AlterField(
            model_name='submission',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Problem'),
        ),
        migrations.DeleteModel(
            name='Album',
        ),
        migrations.DeleteModel(
            name='Song',
        ),
        migrations.AddField(
            model_name='problem',
            name='problemset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Problemset'),
        ),
    ]