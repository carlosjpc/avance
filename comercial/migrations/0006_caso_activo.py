# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-14 23:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0005_auto_20170414_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='caso',
            name='Activo',
            field=models.BooleanField(default=True),
        ),
    ]
