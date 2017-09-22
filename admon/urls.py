# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from admon import views

urlpatterns = [
    # cuenta bancaria
    url(r'^nueva_cuenta_bancaria_agencia/(?P<pk>[0-9]+)/$',
        views.nueva_cuenta_bancaria_agencia,
        name="nueva_cuenta_bancaria_agencia"),
    url(r'editar_cuentab_agencia/(?P<pk>[0-9]+)/$',
        views.editar_cuentab_agencia, name="editar_cuentab_agencia")
]
