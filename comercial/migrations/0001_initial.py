# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agencia_Automotriz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Marca', models.CharField(default='FO', max_length=2, choices=[('AC', 'ACURA'), ('BM', 'BMW'), ('CH', 'CHEVROLET'), ('CY', 'CHRYSLER'), ('FO', 'FORD'), ('HY', 'HYUNDAI'), ('KI', 'KIA'), ('IN', 'INFINITI'), ('IZ', 'ISUZU'), ('MZ', 'MAZDA')])),
                ('Grupo', models.CharField(default='al', max_length=2, choices=[('al', 'ALDEN'), ('ca', 'CAMSA'), ('ce', 'CEVER'), ('da', 'DALTON'), ('so', 'SONNI'), ('ur', 'URIBE'), ('in', 'Independiente')])),
                ('Ciudad', models.CharField(max_length=30)),
                ('Colonia', models.CharField(max_length=30)),
                ('Telefono', models.CharField(max_length=40)),
                ('URL', models.CharField(max_length=40, null=True, blank=True)),
                ('Atiende', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Anotacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Requerimiento', models.TextField(max_length=300)),
                ('Fecha', models.DateTimeField(auto_now_add=True)),
                ('Hecha_por', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Caso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Descripcion', models.TextField(max_length=500)),
                ('Monto', models.PositiveIntegerField()),
                ('Etapa', models.CharField(default='int', max_length=3, choices=[('int', 'Interes'), ('cot', 'Cotizacion Enviada'), ('epa', 'Esperando Papeles'), ('eap', 'Esperando Aprobacion'), ('apr', 'Aprobado'), ('fon', 'Fondeado'), ('crd', 'Cerrado'), ('prd', 'Perdido'), ('rzo', 'Rechazado')])),
                ('Buscar_el', models.DateField()),
                ('Requiere_revision_admon', models.BooleanField(default=False)),
                ('Requiere_revision_vtas', models.BooleanField(default=False)),
                ('Activo', models.BooleanField(default=True)),
                ('Agencia', models.ForeignKey(blank=True, to='comercial.Agencia_Automotriz', null=True)),
                ('Atiende', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('RFC', models.CharField(unique=True, max_length=40)),
                ('Persona_Moral', models.BooleanField(default=True)),
                ('Nombre_Empresa', models.CharField(unique=True, max_length=40)),
                ('Tipo_Negocio', models.CharField(default='SE', max_length=2, choices=[('SE', 'servicios'), ('FA', 'fabricante'), ('CM', 'comercial')])),
                ('Industria', models.CharField(max_length=40)),
                ('Status', models.CharField(default='PR', max_length=2, blank=True, choices=[('PR', 'prospecto'), ('CA', 'cliente activo'), ('CP', 'cliente prospecto'), ('CI', 'cliente inactivo'), ('PF', 'prospecto fallido')])),
                ('Atiende', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contacto_Agencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Nombre_del_Contacto', models.CharField(max_length=40)),
                ('Rol', models.CharField(default='gv', max_length=2, choices=[('dir', 'Director'), ('gv', 'Gerente de Ventas'), ('fi', 'F&I'), ('ve', 'Vendedor')])),
                ('Email', models.EmailField(max_length=254)),
                ('Celular', models.CharField(max_length=40, null=True, blank=True)),
                ('Agencia', models.ForeignKey(to='comercial.Agencia_Automotriz')),
                ('Atiende', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contacto_C',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Nombre_del_Contacto', models.CharField(max_length=40)),
                ('Rol', models.CharField(default='CM', max_length=2, choices=[('RL', 'representante legal'), ('AV', 'aval'), ('CO', 'contador'), ('CM', 'comprador')])),
                ('Email', models.EmailField(max_length=254, null=True, blank=True)),
                ('Telefono', models.CharField(max_length=40, null=True, blank=True)),
                ('Celular', models.CharField(max_length=40, null=True, blank=True)),
                ('Atiende', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
                ('Cliente', models.ForeignKey(to='comercial.Cliente', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Direccion_Fiscal_Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Calle', models.CharField(max_length=140)),
                ('Calle2', models.CharField(max_length=140, null=True, blank=True)),
                ('Colonia', models.CharField(max_length=40)),
                ('Ciudad', models.CharField(default='CDMX', max_length=40)),
                ('Estado', models.CharField(default='CDMX', max_length=40)),
                ('Codigo_Postal', models.PositiveIntegerField()),
                ('Pais', models.CharField(default='Mexico', max_length=40)),
                ('Cliente', models.OneToOneField(to='comercial.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Historial_Etapa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Etapa', models.CharField(default='int', max_length=3, choices=[('int', 'Interes'), ('cot', 'Cotizacion Enviada'), ('epa', 'Esperando Papeles'), ('eap', 'Esperando Aprobacion'), ('apr', 'Aprobado'), ('fon', 'Fondeado'), ('crd', 'Cerrado'), ('prd', 'Perdido'), ('rzo', 'Rechazado')])),
                ('Fecha', models.DateTimeField(auto_now_add=True)),
                ('Caso', models.ForeignKey(to='comercial.Caso', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Interaccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Numero', models.PositiveIntegerField(blank=True)),
                ('Fecha', models.DateTimeField(auto_now_add=True)),
                ('Descripcion', models.TextField(max_length=500)),
                ('Buscar_el', models.DateField()),
                ('Hecha_por', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
                ('Hist_Etapa', models.ForeignKey(to='comercial.Historial_Etapa', blank=True)),
                ('del_Caso', models.ForeignKey(to='comercial.Caso', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='caso',
            name='Cliente',
            field=models.ForeignKey(to='comercial.Cliente', blank=True),
        ),
        migrations.AddField(
            model_name='caso',
            name='Contacto',
            field=models.ForeignKey(to='comercial.Contacto_C', blank=True),
        ),
        migrations.AddField(
            model_name='caso',
            name='Vendedor_Agencia',
            field=models.ForeignKey(blank=True, to='comercial.Contacto_Agencia', null=True),
        ),
        migrations.AddField(
            model_name='anotacion',
            name='Hist_Etapa',
            field=models.ForeignKey(to='comercial.Historial_Etapa', blank=True),
        ),
        migrations.AddField(
            model_name='anotacion',
            name='al_Caso',
            field=models.ForeignKey(to='comercial.Caso', blank=True),
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
