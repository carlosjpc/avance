# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-09 23:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agencia_Automotriz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Marca', models.CharField(choices=[('AC', 'ACURA'), ('BM', 'BMW'), ('CH', 'CHEVROLET'), ('CY', 'CHRYSLER'), ('FO', 'FORD'), ('HY', 'HYUNDAI'), ('KI', 'KIA'), ('IN', 'INFINITI'), ('IZ', 'ISUZU'), ('MZ', 'MAZDA')], default='FO', max_length=2)),
                ('Grupo', models.CharField(choices=[('al', 'ALDEN'), ('ca', 'CAMSA'), ('ce', 'CEVER'), ('da', 'DALTON'), ('so', 'SONNI'), ('ur', 'URIBE'), ('in', 'Independiente')], default='al', max_length=2)),
                ('Ciudad', models.CharField(max_length=30)),
                ('Colonia', models.CharField(max_length=30)),
                ('Telefono', models.CharField(max_length=40)),
                ('URL', models.CharField(blank=True, max_length=40, null=True)),
                ('Atiende', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Anotacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Requerimiento', models.TextField(max_length=300)),
                ('Fecha', models.DateField(auto_now_add=True)),
                ('Hecha_por', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Caso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Descripcion', models.TextField(max_length=500)),
                ('Monto', models.PositiveIntegerField()),
                ('Etapa', models.CharField(choices=[('int', 'Interes'), ('cot', 'Cotizacion Enviada'), ('epa', 'Esperando Papeles'), ('eap', 'Esperando Aprobacion'), ('apr', 'Aprobado'), ('fon', 'Fondeado'), ('crd', 'Cerrado'), ('prd', 'Perdido')], default='int', max_length=3)),
                ('Buscar_el', models.DateField()),
                ('Requiere_revision', models.BooleanField(default=False)),
                ('Agencia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comercial.Agencia_Automotriz')),
                ('Atiende', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RFC', models.CharField(max_length=40, unique=True)),
                ('Persona_Moral', models.BooleanField(default=True)),
                ('Nombre_Empresa', models.CharField(max_length=40, unique=True)),
                ('Tipo_Negocio', models.CharField(choices=[('SE', 'servicios'), ('FA', 'fabricante'), ('CM', 'comercial')], default='SE', max_length=2)),
                ('Industria', models.CharField(max_length=40)),
                ('Status', models.CharField(blank=True, choices=[('PR', 'prospecto'), ('CA', 'cliente activo'), ('CP', 'cliente prospecto'), ('CI', 'cliente inactivo'), ('PF', 'prospecto fallido')], default='PR', max_length=2)),
                ('Atiende', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contacto_Agencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre_del_Contacto', models.CharField(max_length=40)),
                ('Rol', models.CharField(choices=[('dir', 'Director'), ('gv', 'Gerente de Ventas'), ('fi', 'F&I'), ('ve', 'Vendedor')], default='gv', max_length=2)),
                ('Email', models.EmailField(max_length=254)),
                ('Celular', models.CharField(blank=True, max_length=40, null=True)),
                ('Agencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comercial.Agencia_Automotriz')),
                ('Atiende', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contacto_C',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre_del_Contacto', models.CharField(max_length=40)),
                ('Rol', models.CharField(choices=[('RL', 'representante legal'), ('AV', 'aval'), ('CO', 'contador'), ('CM', 'comprador')], default='CM', max_length=2)),
                ('Email', models.EmailField(blank=True, max_length=254, null=True)),
                ('Telefono', models.CharField(blank=True, max_length=40, null=True)),
                ('Celular', models.CharField(blank=True, max_length=40, null=True)),
                ('Cliente', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='comercial.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Direccion_Fiscal_Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Calle', models.CharField(max_length=140)),
                ('Calle2', models.CharField(blank=True, max_length=140, null=True)),
                ('Colonia', models.CharField(max_length=40)),
                ('Ciudad', models.CharField(default='CDMX', max_length=40)),
                ('Estado', models.CharField(default='CDMX', max_length=40)),
                ('Codigo_Postal', models.PositiveIntegerField()),
                ('Pais', models.CharField(default='Mexico', max_length=40)),
                ('Cliente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='comercial.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Interaccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Numero', models.PositiveIntegerField(blank=True)),
                ('Fecha', models.DateField(auto_now_add=True)),
                ('Descripcion', models.TextField(max_length=500)),
                ('Buscar_el', models.DateField()),
                ('Hecha_por', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('del_Caso', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='comercial.Caso')),
            ],
        ),
        migrations.AddField(
            model_name='caso',
            name='Cliente',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='comercial.Cliente'),
        ),
        migrations.AddField(
            model_name='caso',
            name='Contacto',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='comercial.Contacto_C'),
        ),
        migrations.AddField(
            model_name='caso',
            name='Vendedor_Agencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comercial.Contacto_Agencia'),
        ),
        migrations.AddField(
            model_name='anotacion',
            name='al_Caso',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='comercial.Caso'),
        ),
        migrations.AlterUniqueTogether(
            name='contacto_c',
            unique_together=set([('Cliente', 'Nombre_del_Contacto')]),
        ),
        migrations.AlterUniqueTogether(
            name='contacto_agencia',
            unique_together=set([('Agencia', 'Email')]),
        ),
        migrations.AlterUniqueTogether(
            name='agencia_automotriz',
            unique_together=set([('Marca', 'Grupo', 'Colonia')]),
        ),
    ]
