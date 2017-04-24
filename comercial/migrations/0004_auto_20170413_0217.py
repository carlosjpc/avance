# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-13 02:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0003_historial_etapa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caso',
            name='Etapa',
            field=models.CharField(choices=[('int', 'Interes'), ('cot', 'Cotizacion Enviada'), ('epa', 'Esperando Papeles'), ('eap', 'Esperando Aprobacion'), ('apr', 'Aprobado'), ('fon', 'Fondeado'), ('crd', 'Cerrado'), ('prd', 'Perdido'), ('rzo', 'Rechazado')], default='int', max_length=3),
        ),
        migrations.AlterField(
            model_name='historial_etapa',
            name='Etapa',
            field=models.CharField(choices=[('int', 'Interes'), ('cot', 'Cotizacion Enviada'), ('epa', 'Esperando Papeles'), ('eap', 'Esperando Aprobacion'), ('apr', 'Aprobado'), ('fon', 'Fondeado'), ('crd', 'Cerrado'), ('prd', 'Perdido'), ('rzo', 'Rechazado')], default='int', max_length=3),
        ),
    ]