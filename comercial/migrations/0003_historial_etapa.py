# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-13 02:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0002_contacto_c_atiende'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historial_Etapa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Etapa', models.CharField(choices=[('int', 'Interes'), ('cot', 'Cotizacion Enviada'), ('epa', 'Esperando Papeles'), ('eap', 'Esperando Aprobacion'), ('apr', 'Aprobado'), ('fon', 'Fondeado'), ('crd', 'Cerrado'), ('prd', 'Perdido')], default='int', max_length=3)),
                ('Fecha', models.DateField(auto_now_add=True)),
                ('Caso', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='comercial.Caso')),
            ],
        ),
    ]
