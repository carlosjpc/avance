# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from central import views

urlpatterns = [
    url(r'^contrato_maestro_pmoral_pdf/$', views.contrato_maestro_pmoral_pdf,
        name="contrato_maestro_pmoral_pdf"),
]
