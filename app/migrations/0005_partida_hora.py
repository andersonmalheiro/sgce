# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-22 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20180521_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='hora',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Hora'),
        ),
    ]
