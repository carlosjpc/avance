# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-10 03:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comercial', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacto_c',
            name='Atiende',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
