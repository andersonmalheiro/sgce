# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-01 14:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partida',
            name='grupo',
        ),
    ]
