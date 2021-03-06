# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='site',
            field=models.URLField(blank=True, null=True),
        ),
    ]
