# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-21 00:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('central', '0003_auto_20170418_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentacion_pmoral',
            name='Anexo',
        ),
        migrations.RemoveField(
            model_name='documentacion_pmoral',
            name='Contrato',
        ),
        migrations.AddField(
            model_name='documentacion_pmoral',
            name='Identificacion_Rep_Aval',
            field=models.BooleanField(default=False),
        ),
    ]